// Wait until the DOM content is fully loaded before executing scripts.
document.addEventListener("DOMContentLoaded", function () {

    // -------------------------------------------
    // Navigation: Highlight active link
    // -------------------------------------------
    const navLinks = document.querySelectorAll("nav ul li a");
    const currentPath = window.location.pathname.split("/").pop() || "index.html";
  
    navLinks.forEach(function (link) {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
      }
    });
  
    // -------------------------------------------
    // Signup Form Validation: Check matching passwords
    // -------------------------------------------
    const signupForm = document.querySelector("form[action='/signup']");
    if (signupForm) {
      signupForm.addEventListener("submit", function (event) {
        const passwordField = document.getElementById("password");
        const confirmPasswordField = document.getElementById("confirm_password");
  
        if (passwordField && confirmPasswordField && passwordField.value !== confirmPasswordField.value) {
          event.preventDefault();
          alert("Passwords do not match. Please try again.");
          passwordField.focus();
        }
      });
    }
  
    // -------------------------------------------
    // Loan Application Form: Validation, Interest Rate Calculation,
    // and Same-Page Response Display
    // -------------------------------------------
    const loanForm = document.querySelector("form[action='/apply-loan']");
    if (loanForm) {
      loanForm.addEventListener("submit", function (event) {
        // Prevent default submission so that we remain on the same page.
        event.preventDefault();
        
        // Validate loan amount
        const amountInput = document.getElementById("amount");
        const amount = parseFloat(amountInput.value);
        if (isNaN(amount) || amount <= 0) {
          alert("Please enter a valid positive number for the loan amount.");
          amountInput.focus();
          return;
        }
        
        // Validate credit score: ensure provided value is a number and at least 650.
        const creditScoreInput = document.getElementById("credit_score");
        const creditScore = parseInt(creditScoreInput.value, 10);
        if (isNaN(creditScore) || creditScore < 650) {
          alert("Your credit score must be at least 650 to apply for a loan.");
          creditScoreInput.focus();
          return;
        }
        
        // Determine interest rate based on credit score thresholds.
        let interestRate;
        if (creditScore >= 800) {
          interestRate = 3.5;
        } else if (creditScore >= 750) {
          interestRate = 4.0;
        } else {
          interestRate = 5.0;
        }
        
        // Optionally update a hidden field if sending the rate to the backend.
        const interestRateField = document.getElementById("interest_rate");
        if (interestRateField) {
          interestRateField.value = interestRate;
        }
        
        // Prepare the response message.
        const responseMessage = `
          <p>Your loan application qualifies!</p>
          <p>Based on your credit score of ${creditScore}, your interest rate is <strong>${interestRate}%</strong>.</p>
          <p>Loan Amount Requested: ₹${amount.toLocaleString()}</p>
        `;
        
        // Output the message on the same page within a dedicated container.
        let responseContainer = document.getElementById("loan_response");
        if (!responseContainer) {
          responseContainer = document.createElement("div");
          responseContainer.id = "loan_response";
          loanForm.parentNode.insertBefore(responseContainer, loanForm.nextSibling);
        }
        responseContainer.innerHTML = responseMessage;
      });
    }
  
    // -------------------------------------------
    // Transfer Funds Form: Validate fields and prompt for Transaction PIN
    // -------------------------------------------
    const transferForm = document.querySelector("form[action='/transfer-funds']");
    if (transferForm) {
      transferForm.addEventListener("submit", function (event) {
        event.preventDefault();
        
        // Retrieve the values from the form.
        const accountNumber = document.getElementById("account_number").value.trim();
        const accountNumberConfirm = document.getElementById("account_number_confirm").value.trim();
        const ifsc = document.getElementById("ifsc").value.trim();
        const amountInput = document.getElementById("transfer_amount").value.trim();
        
        // Validate both account number entries.
        if (!accountNumber || !accountNumberConfirm) {
          alert("Please enter the recipient's account number in both fields.");
          return;
        }
        if (accountNumber !== accountNumberConfirm) {
          alert("The account numbers do not match. Please check and try again.");
          return;
        }
        
        // Validate that the IFSC code is provided.
        if (!ifsc) {
          alert("Please provide a valid IFSC code.");
          return;
        }
        
        // Validate the transfer amount is a positive number.
        const amount = parseFloat(amountInput);
        if (isNaN(amount) || amount <= 0) {
          alert("Please enter a valid, positive transfer amount.");
          return;
        }
        
        // Prompt the user to enter the transaction PIN.
        const txnPin = prompt("Enter your transaction PIN:");
        if (txnPin === null) {
          // User canceled the prompt.
          return;
        }
        
        // Retrieve the container for displaying the transaction result.
        const responseContainer = document.getElementById("transfer_response");
        
        // Check whether the entered PIN is exactly "0000".
        if (txnPin !== "0000") {
          responseContainer.innerHTML = "<p style='color:red;'>Transaction failed: Incorrect transaction PIN.</p>";
          return;
        }
        
        // On success, display a confirmation message.
        responseContainer.innerHTML = `<p style='color:green;'>Funds transferred successfully to account ${accountNumber} for an amount of ₹${amount.toLocaleString()}. IFSC: ${ifsc}</p>`;
      });
    }
  
    // -------------------------------------------
    // Login Form Check: Validate that username/email is entered.
    // -------------------------------------------
    const loginForm = document.querySelector("form[action='/login']");
    if (loginForm) {
      loginForm.addEventListener("submit", function (event) {
        const usernameInput = document.getElementById("username");
        if (usernameInput && !usernameInput.value.trim()) {
          event.preventDefault();
          alert("Please enter your username or email.");
          usernameInput.focus();
        }
      });
    }
  
  });  