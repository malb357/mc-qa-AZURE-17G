Feature: GenerateBilling with parameters and billing files generation

 Scenario: MCAZURE-47 GenerateBilling - Parametro force con valor true
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is OK

 Scenario: MCAZURE-48 GenerateBilling - Parametro force con valor false
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with value false is executed with boto
    Then the answer to the lambda generateBilling is OK

 Scenario: MCAZURE-499a GenerateBilling - Parametro offset_a
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with "{offset_a}" is executed with boto
    Then the answer to the lambda generateBilling is OK
    and billed detail files with "{offset_a}" exists

 Scenario: MCAZURE-499b GenerateBilling - Parametro offset_b
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with "{offset_b}" set is executed with boto
    Then the answer to the lambda generateBilling is OK
    and detail files with "{offset_b}" exists

Scenario: MCAZURE-500 GenerateBilling - Parametro offset menor que 0
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with offset <0 is executed with boto
    Then the answer to the lambda generateBilling is 400

Scenario: MCAZURE-501 GenerateBilling - Parametro offset invalido
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with offset invalid is executed with boto
    Then the answer to the lambda generateBilling is 400

 Scenario: MCAZURE-177 GenerateBilling - Autenticacion usuario admin
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is OK

 Scenario: MCAZURE-31 GenerateBilling - PriceFactor update
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    And priceFactor is updated with "{newPriceFactor}" in DynamoDB
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is OK
    And restore priceFactor in DynamoDB

 Scenario: MCAZURE-35 GenerateBilling - PriceFactor invalido
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    And priceFactor is updated with invalidPriceFactor "{invalidPriceFactor}" in DynamoDB
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is 500
    And restore priceFactor in DynamoDB

 Scenario: MCAZURE-65 GenerateBilling - Bucket invalido
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    And BucketName is updated with invalidBucketName in DynamoDB
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is 500
    And restore bucketName in DynamoDB

 Scenario: MCAZURE-50 GenerateBilling - Language updated ES
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    And language is updated with ES in DynamoDB
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today summary file is downloaded
    And summary file header were correctly generated
    And today detail file is downloaded
    And detail file header were correctly generated
    And restore language in DynamoDB

 Scenario: MCAZURE-54 GenerateBilling - Language updated EN
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    And language is updated with EN in DynamoDB
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today summary file is downloaded
    And summary file header were correctly generated
    And today detail file is downloaded
    And detail file header were correctly generated
    And restore language in DynamoDB

 Scenario: MCAZURE-56 GenerateBilling - Language updated INVALID
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    And language is updated with INVALID in DynamoDB
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is 500
    And restore language in DynamoDB

 Scenario: MCAZURE-332a GenerateBilling - Parametro exchangeRate = 0
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with value exchangeRate = 0 is executed with boto
    Then the answer to the lambda generateBilling is OK

 Scenario: MCAZURE-332b GenerateBilling - Parametro exchangeRate > 0
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with value exchangeRate > 0 is executed with boto
    Then the answer to the lambda generateBilling is OK

 Scenario: MCAZURE-334 GenerateBilling - Parametro exchangeRate < 0
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with value exchangeRate < 0 is executed with boto
    Then the answer to the lambda generateBilling is 400

 Scenario: MCAZURE-335 GenerateBilling - Parametro exchangeRate invalid
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with invalid exchangeRate is executed with boto
    Then the answer to the lambda generateBilling is 400

 Scenario: MCAZURE-339 GenerateBilling - Comprobar redondeo a 2 decimales de los campos del fichero summary
    Given an AWS admin user
    And an aws credentials for s3
    And a OB with an AWS account
    When generateBilling with force with value true is executed with boto
    Then the answer to the lambda generateBilling is OK
    And today summary file is downloaded
    And summary file fields have 2 decimals

