from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "customers.db"


# ----------------------------
# Database Connection
# ----------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def home():

    conn = get_db()

    customers = conn.execute(
        "SELECT * FROM customers ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        customers=customers
    )


# ----------------------------
# Add Customer
# ----------------------------
@app.route("/add", methods=["GET", "POST"])
def add_customer():

    if request.method == "POST":

        name = request.form["name"]
        number = request.form["number"]
        address = request.form["address"]
        brand = request.form["brand"]
        camera = request.form["camera"]
        install_date = request.form["install_date"]
        next_service = request.form["next_service"]
        status = request.form["status"]

        conn = get_db()

        conn.execute(
            """
            INSERT INTO customers
            (name,number,address,brand,camera,install_date,next_service,status)

            VALUES
            (?,?,?,?,?,?,?,?)
            """,
            (
                name,
                number,
                address,
                brand,
                camera,
                install_date,
                next_service,
                status,
            ),
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_customer.html")


# ----------------------------
# Edit Customer
# ----------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        number = request.form["number"]
        address = request.form["address"]
        brand = request.form["brand"]
        camera = request.form["camera"]
        install_date = request.form["install_date"]
        next_service = request.form["next_service"]
        status = request.form["status"]

        conn.execute(
            """
            UPDATE customers

            SET

            name=?,
            number=?,
            address=?,
            brand=?,
            camera=?,
            install_date=?,
            next_service=?,
            status=?

            WHERE id=?
            """,
            (
                name,
                number,
                address,
                brand,
                camera,
                install_date,
                next_service,
                status,
                id,
            ),
        )

        conn.commit()
        conn.close()

        return redirect("/")

    customer = conn.execute(
        "SELECT * FROM customers WHERE id=?",
        (id,),
    ).fetchone()

    conn.close()

    return render_template(
        "edit_customer.html",
        customer=customer,
    )


# ----------------------------
# Delete Customer
# ----------------------------
@app.route("/delete/<int:id>")
def delete_customer(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM customers WHERE id=?",
        (id,),
    )

    conn.commit()
    conn.close()

    return redirect("/")


# ----------------------------
# Search Customer
# ----------------------------
@app.route("/search")
def search():

    keyword = request.args.get("q", "")

    conn = get_db()

    customers = conn.execute(
        """
        SELECT *

        FROM customers

        WHERE

        name LIKE ?
        OR number LIKE ?
        OR status LIKE ?

        ORDER BY id DESC
        """,
        (
            "%" + keyword + "%",
            "%" + keyword + "%",
            "%" + keyword + "%",
        ),
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        customers=customers,
    )


# ----------------------------
# Run App
# ----------------------------
# ----------------------------
# ----------------------------
# Customer Details
# ----------------------------
@app.route("/customer/<int:id>")
def customer_details(id):

    conn = get_db()

    customer = conn.execute(
        "SELECT * FROM customers WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "customer_details.html",
        customer=customer
    )


# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)