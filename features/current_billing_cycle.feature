Feature: MCAZURE-4929 generate current billing cycle file

  Scenario: Success - Generate current billing cycle summary file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When currentBillingCycle is executed with boto
    Then the answer to the lambda currentBillingCycle is OK
    And today current billing cycle summary file is downloaded
    And today current billing cycle detail file is downloaded
    And consumption file is downloaded
    And charge current billing summary value is correct

  Scenario: Success - Remove optional items current billing cycle summary file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When currentBillingCycle with includeRef with value false is executed with boto
    Then the answer to the lambda currentBillingCycle is OK
    And today current billing cycle summary file is downloaded
    And current billing cycle summary file header were correctly generated

  Scenario: Success - Include optional current billing cycle items summary file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When currentBillingCycle with includeRef with value true is executed with boto
    Then the answer to the lambda currentBillingCycle is OK
    And today current billing cycle summary file is downloaded
    And current billing cycle summary file header were correctly generated

  Scenario: Success - Generate current billing cycle detail file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When currentBillingCycle is executed with boto
    Then the answer to the lambda currentBillingCycle is OK
    And today current billing cycle detail file is downloaded 
    And consumption file is downloaded
    And charge current billing detail value is correct

  Scenario: Success - Remove optional items current billing cycle detail file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When currentBillingCycle with includeRef with value false is executed with boto
    Then the answer to the lambda currentBillingCycle is OK
    And today current billing cycle detail file is downloaded
    And current billing cycle detail file header with remove headers were correctly generated

  Scenario: Success - Include optional items current billing detail file
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When currentBillingCycle with includeRef with value true is executed with boto
    Then the answer to the lambda currentBillingCycle is OK
    And today current billing cycle detail file is downloaded
    And current billing cycle detail file header with headers were correctly generated
