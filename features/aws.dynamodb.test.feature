Feature: Aws dynamoDB Test

  Scenario: aws dynamodb test
    Given an aws credentials for dynamodb
     When the database "aws-users-int-mc" is not empty
     Then the content of the db is shown


