locals {
  common_vars = read_terragrunt_config(find_in_parent_folders("common.hcl"))

  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))

  region_vars = read_terragrunt_config(find_in_parent_folders("region.hcl"))


  account_id       = local.account_vars.locals.account_id
  state_key_prefix = local.account_vars.locals.state_key_prefix
  state_role_arn   = local.account_vars.locals.state_role_arn
  region           = local.region_vars.locals.region

  root_account_id = 732617013467
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
    region  = "${local.region}"
    allowed_account_ids = ["${local.account_id}"]
}
EOF
}

remote_state {
  backend = "s3"
  config = {
    encrypt        = true
    bucket         = "tf-state-${local.account_id}"
    key            = "${local.state_key_prefix}/${path_relative_to_include()}/terraform.tfstate"
    role_arn       = "${local.state_role_arn}"
    region         = "eu-west-2"
    dynamodb_table = "tf-state-${local.account_id}"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

inputs = merge(
  {
    namespace = "backups"
  },
  local.common_vars.locals,
  local.account_vars.locals,
  local.region_vars.locals
)