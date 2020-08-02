Feature: GenerateBilling summary file generation

  Scenario: Success - Generate summary file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today summary file is downloaded
    And the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info

  Scenario: Success - Remove optional items
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with includeRef with value false is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today summary file is downloaded
    And summary file header were correctly generated
    And the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info

  Scenario: Success - Include optional items
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with includeRef with value true is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today summary file is downloaded
    And summary file header were correctly generated
    And the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info




