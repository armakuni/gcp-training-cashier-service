Feature: Withdraw or Deposit balance into an account
  As a client
  I want to withdraw or deposit balance into an account

  Scenario: Deposit cash
    When I make a "credit" request for amount 120 to account "12345678"
    Then I should receive an "Accepted" response
    And a "credit" request should have been published for account "12345678" with amount 120

    Scenario: Withdraw cash
      When I make a "debit" request for amount 50 to account "98765432"
      Then I should receive an "Accepted" response
      And a "debit" request should have been published for account "98765432" with amount 50
