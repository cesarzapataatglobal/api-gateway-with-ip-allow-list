
module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "~> 2.0"

  function_name = "ip-allow-list-authorizer-${local.environment}"
  handler       = "authorizer.lambda_handler"
  runtime       = "python3.8"
  source_path = [
    "lambda-functions/ip-allow-list-authorizer/src/authorizer.py",
    {
      pip_requirements = "lambda-functions/ip-allow-list-authorizer/src/requirements.txt"
    }
  ]

  vpc_subnet_ids         = module.vpc.private_subnets
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  attach_network_policy  = true

  publish = true

  environment_variables = {
    ALLOWED_CIDRS = join(",", var.allowed_cidrs)
  }

  allowed_triggers = {
    AllowExecutionFromAPIGatewayAuthorizer = {
      service    = "apigateway"
      source_arn = "${module.api_gateway.this_apigatewayv2_api_execution_arn}/authorizers/${aws_apigatewayv2_authorizer.this.id}"
    }
  }
}
