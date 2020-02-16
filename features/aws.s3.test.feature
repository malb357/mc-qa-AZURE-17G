Feature: Aws S3 Test

  Scenario: aws s3 test
    Given an aws credentials for s3
     When the bucket "prebilling-aws-qa-mc" is not empty
     Then a list of objects names are shown


