document.querySelectorAll("[data-login]").forEach((button) => {
  button.addEventListener("click", () => {
    const email = document.querySelector("input[name='email']");
    const senha = document.querySelector("input[name='senha']");
    if (email && senha) {
      email.value = button.dataset.login;
      senha.value = "123456";
    }
  });
});

document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm)) {
      event.preventDefault();
    }
  });
});
