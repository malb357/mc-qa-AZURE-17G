Feature: GenerateBilling detail file generation

  Scenario: MCAZURE-4702 generateBilling - Headers detail file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today detail file is downloaded
    And detail file header were correctly generated
    And the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info
  

  Scenario: MCAZURE-4941 - Remove optional items in detail file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with includeRef with value false is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today detail file is downloaded
    And detail file header were correctly generated
    And the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info




