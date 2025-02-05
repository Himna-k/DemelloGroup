document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchButton').addEventListener('click', function () {
      const domainInput = document.getElementById('domainInput').value.trim(); 
      if (domainInput) {
        const redirectUrl = `https://www.secureserver.net/products/domain-registration/find?plid=502685&domainToCheck=${domainInput}`;
        
window.location.href = redirectUrl;
      } else {
        alert('Please enter a domain name.');
      }
    });
  });
  
