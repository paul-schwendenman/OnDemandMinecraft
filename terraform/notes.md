# Terraform Intro

## Setup

1. Instalation

       $ brew install terraform

2. Configure terraform

       $ terraform init

3. Generates an execution plan

       $ terraform plan --out plan.out

4. Change or build infrastructure

       $ terraform apply "plan.out"

## Other

Show Outputs:

    $ terraform output

Trigger Regeneration of EC2 instance:

    $ terraform taint aws_instance.web

# Heroku

Installation:

    $ brew tap heroku/brew && brew install heroku

Config:

    $ heroku config:set AWS_ACCESS_KEY_ID=AAAAAAAAAAAAAAA
    $ heroku config:set AWS_SECRET_ACCESS_KEY=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
