document.addEventListener("DOMContentLoaded", function () {
    emailjs.init("MRI0ZXAvw4uAYCs3X"); // Replace with your EmailJS user ID
});

const step1 = document.querySelector(".step1"),
    step2 = document.querySelector(".step2"),
    step3 = document.querySelector(".step3"),
    emailAddress = document.getElementById("emailAddress"),
    verifyEmail = document.getElementById("verifyEmail"),
    inputs = document.querySelectorAll(".otp-group input"),
    nextButton = document.getElementById("sendOtpButton"),
    verifyButton = document.getElementById("verifyButton"),
    getStartedButton = document.getElementById("getStartedButton");

let OTP = ""; // Store the generated OTP
 

const validateEmail = (email) => {

    let re = /\S+@\S+\.\S+/;
    if (re.test(email)) {
        nextButton.classList.remove("disable");
    } else {
        nextButton.classList.add("disable");
    }
};

emailAddress.addEventListener("input", () => {
    validateEmail(emailAddress.value);
});

inputs.forEach((input, index) => {
    input.addEventListener("keyup", function (e) {
        // Move to the next input field if the current one has a value
        if (this.value.length >= 1) {
            e.target.value = e.target.value.substr(0, 1);
            // Move to the next input field
            if (index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        }

        // Check if all OTP fields are filled
        if ([...inputs].every(input => input.value !== "")) {
            verifyButton.classList.remove("disable");
        } else {
            verifyButton.classList.add("disable");
        }
    });
});

const serviceID = "service_qypj3br"; // Replace with your actual service ID
const templateID = "template_jmz3xut";// Replace with your actual template ID

nextButton.addEventListener("click", () => {
    OTP = Math.floor(1000 + Math.random() * 9000).toString(); // Generate a 4-digit OTP
    nextButton.innerHTML = "&#9889; Sending...";

    let templateParameter = {
        from_name: "dR",
        OTP: OTP,
        to_email: emailAddress.value // Send OTP to the email entered by the user
    };

    emailjs.send(serviceID, templateID, templateParameter).then(
        (res) => {
            console.log(res,"hi");
            nextButton.innerHTML = "Next &rarr;";
            step1.style.display = "none";
            step2.style.display = "block";   // Show step2 after sending email
            verifyEmail.textContent = emailAddress.value;
        },
        (err) => {
            console.log(err);
        }
    );
});

verifyButton.addEventListener("click", async() => {
    console.log("HELLO");
    let values = ""; // Initialize values
    inputs.forEach((input) => { // Use 'inputs' instead of 'input'
        values += input.value; // Concatenate the values to form the OTP
    });
    
    
    // Check if the constructed OTP matches the generated OTP
    if (OTP === values) {
        const response = await fetch("/login_otp");
        step2.style.display = "none"; // Hide step2 on success
        step3.style.display = "block"; // Show step3 on success
    } else {
        verifyButton.classList.add("error-shake"); // Add error shake class for feedback
    }
    
    setTimeout(() => {
        verifyButton.classList.remove("error-shake"); // Remove class after some time
    }, 1000);
});

// Add event listener for the "Get Started" button
getStartedButton.addEventListener("click", () => {
    window.location.href = "/index"; // Redirect to the home page or any other page
});