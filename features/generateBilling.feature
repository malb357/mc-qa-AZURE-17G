Feature: GenerateBilling

  Scenario: Success - Generate files
    Given an AWS admin user
    And a OB with an AWS account
    When generateBilling is executed with boto
    Then the answer to the lambda generateBilling is OK
    Then today summary, a client and a detail file are downloaded
    Then the lastAWSInvoiceDate and BillingFileDate from DynamoDB is updated with the last billing info


