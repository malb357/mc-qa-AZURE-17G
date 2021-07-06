Feature: GenerateBilling subsummary file generation

  Scenario: MCAZURE-4707 Success - Generate subsummary file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today subsummary file is downloaded
    And subsummary file header were correctly generated
    And the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info

