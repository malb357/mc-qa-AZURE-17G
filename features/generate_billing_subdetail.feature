Feature: GenerateBilling subdetail file generation

  Scenario: MCAZURE-4709 Success - Generate subdetail file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today subdetail file is downloaded
    And subdetail file header were correctly generated
    And the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info