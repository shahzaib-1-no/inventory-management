# Django Inventory Management System

A complete **Inventory Management System** built with **Django** and **PostgreSQL**. This project helps businesses manage **stock, sales, purchase, and reporting** efficiently. Perfect for **students, developers, and small businesses** looking for a free open-source solution.

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Framework-Django-092E20?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/License-GPLv3-yellow?logo=gnu" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Build-Passing-brightgreen?logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/github/issues/shahzaib-1-no/inventory-management?color=orange&logo=github" />
  <img src="https://img.shields.io/github/stars/shahzaib-1-no/inventory-management?logo=github" />
  <img src="https://img.shields.io/github/forks/shahzaib-1-no/inventory-management?logo=github" />
  <img src="https://img.shields.io/github/last-commit/shahzaib-1-no/inventory-management?logo=git" />
  <img src="https://img.shields.io/github/repo-size/shahzaib-1-no/inventory-management?logo=github" />
</p>

<!-- Build / Quality / Security / Maintenance Badges -->
<p align="center">

  <!-- Build Status -->
  <img src="https://github.com/shahzaib-1-no/inventory-management/actions/workflows/django.yml/badge.svg" />
  <!-- Code Coverage -->
  <a href="https://codecov.io/gh/shahzaib-1-no/inventory-management">
    <img src="https://codecov.io/gh/shahzaib-1-no/inventory-management/branch/main/graph/badge.svg" />
  </a>
  <!-- Code Quality -->
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" />
  </a>
  <img src="https://img.shields.io/badge/lint-Flake8-blue" />
  <img src="https://img.shields.io/badge/lint-Pylint-yellow" />
  <!-- Security -->
  <a href="https://snyk.io/test/github/shahzaib-1-no/inventory-management">
    <img src="https://snyk.io/test/github/shahzaib-1-no/inventory-management/badge.svg" />
  </a>
  <img src="https://img.shields.io/badge/security-Bandit-red" />
  <!-- Maintenance -->
  <img src="https://img.shields.io/github/contributors/shahzaib-1-no/inventory-management" />

</p>

---

## 📚 Table of Contents

- [🚀 Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📈 Use Cases](#-use-cases)
- [⚙️ Installation Guide](#️-installation-guide)
- [📸 Screenshots](#-screenshots)
- [📝 Changelog](#-changelog)
- [📜 License](#-license)
- [🤝 Contributing](#-contributing)
- [🔒 Security](#-security)
- [⭐ Support](#-support)
- [👨‍💻 Author](#-author)

---

## 🚀 Features

- 📦 **Stock Management** – Add, update, and track inventory in real-time _(Planned Feature)_.
- 💰 **Sales Management** – Record sales transactions and generate invoices _(Planned Feature)_.
- 🛒 **Purchase Management** – Manage supplier purchases and expenses _(Planned Feature)_.
- 🤝 **Supplier Management** – Maintain supplier profiles, contact details, and transaction history _(Planned Feature)_.
- 📊 **Reports & Analytics** – Generate daily, monthly, and custom reports using Chart.js _(Planned Feature)_.
- 👤 **User Management** – Manage users, roles, and permissions (RBAC integration).
- 🔐 **Secure Authentication** – Django’s built-in auth system with login/logout and role-based access.
- 📁 **Role-Based Access Control (RBAC)** – Fine-grained permission handling for each module.
- ⚙️ **Dynamic DataTables Integration** – Server-side pagination, sorting, and searching.
- 🚨 **SweetAlert Integration** – Elegant alerts for confirmations and success/error messages.
- 🧾 **Export & Reporting** – Export data to Excel or PDF for business analytics _(Planned Feature)_.
- 🧱 **Modular Architecture** – Organized Django apps for Users, Roles, Products, Sales, and Purchases.
- 🌐 **Dockerized Setup** – Pre-configured Docker environment for local and production use.
- 🧩 **Responsive Dashboard** – Clean, mobile-friendly UI built with Bootstrap 5.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python 3.9+) with Django ORM
- **Database:** PostgreSQL
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript (ES6)
- **Libraries & Tools:**
  - Chart.js → For interactive charts and reports
  - DataTables → For server-side data tables
  - SweetAlert2 → For confirmation dialogs and alerts
  - Django Environ → For environment variable management
  - Django Debug Toolbar → For debugging in development
- **Authentication & Authorization:** Django Auth System + Built-in RBAC
- **Containerization:** Docker & Docker Compose
- **Code Quality:** Black, Flake8, isort
- **Version Control:** Git & GitHub

---

## 📈 Use Cases

- Small shops & businesses to manage stock and sales
- Students learning Django + PostgreSQL projects
- Developers building POS or ERP-like systems
- Open-source learning reference

---

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/shahzaib-1-no/inventory-management.git
   cd inventory-management
   ```

2. **Create virtual environment & activate**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database (PostgreSQL)**

   - Create a PostgreSQL database (example: `inventory_db`).
   - Update settings in `settings.py`.

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Start server**
   ```bash
   python manage.py runserver
   ```

---

## 📸 Screenshots

(Add screenshots or GIFs of your project UI here for better impact on portfolio & ranking)

---

## 📜 Changelog

- **v1.0.0** – Initial release with stock, sales, purchase & reporting.
- **v1.1.0** – Added user roles & PostgreSQL support.
- **v1.2.0** – Improved reports and bug fixes.

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.
You must give appropriate credit by mentioning the author **[Shahzaib Ali](https://github.com/shahzaib-1-no)** whenever using this project.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo, submit issues, or create pull requests.

---

## 🔒 Security

If you discover any security issues, please report them via email instead of creating a public issue.

---

## ⭐ Support

If you like this project, please **star the repository** on GitHub. It helps others find it and supports the project growth.

---

## 🔹 Author

👨‍💻 Created & maintained by [Shahzaib Ali](https://github.com/shahzaib-1-no)
📬 For collaboration or freelance work: **sa4715228@gmail.com**
