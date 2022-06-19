#config file containing credentials for RDS MySQL instance
db_username = "admin"
db_password = "perMysql2358!"
db_name = "testSchema"

"""
aws lambda create-function --function-name  CreateTableAddRecordsAndRead --runtime python3.9 --zip-file fileb://app.zip --handler app.handler --role arn:aws:iam::035974012754:role/lambda-vpc-role --vpc-config SubnetIds=subnet-0a7393ad6c6ff1f09,subnet-03cb983e2e025a34f,SecurityGroupIds=sg-00fbec1bdf6a0273a
"""