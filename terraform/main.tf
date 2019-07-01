provider "aws" {
  version = "~> 2.0"
  region  = "${var.region}"
}

provider "tls" {
  version = "~> 2.0"
}

provider "local" {
  version = "~> 1.3"
}

provider "heroku" {
  version = "~> 2.0"
}

locals {
    private_key_filename = "${var.key_name}.pem"
}
