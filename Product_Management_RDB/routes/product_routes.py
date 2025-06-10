from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from models.product import Product
from models.subproduct import SubProduct
from models.category import Category
from models.supplier import Supplier
from flask_login import current_user
from models.plant_brand import PlantBrand

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/')
def view_products():
    products = Product.query.all()
    return render_template('product_templates/view_products.html', products=products)

# @product_bp.route('/<int:product_id>')
# def product_details(product_id):
#     product = Product.query.get_or_404(product_id)
#     return render_template('product_templates/product_details.html', product=product)


# @product_bp.route('/add', methods=['GET', 'POST'])
# @login_required
# def add_product():
#     if request.method == 'POST':
#         name = request.form['name']
#         category = request.form['category']  # Enum value as string
#         cost = request.form['cost']
#         version = request.form['version']
#         description = request.form['description']
#         brand_id = request.form['brand_id']  # Selected brand from dropdown

#         product = Product(
#             name=name,
#             category=category,
#             cost=cost,
#             version=version,
#             description=description,
#             supplier_id=current_user.id,
#             plant_brand_id=brand_id
#         )
#         db.session.add(product)
#         db.session.commit()
#         flash('Product added successfully!', 'success')
#         return redirect(url_for('product.view_products'))

#     # Enum categories (hardcoded list)
#     categories = ['Operating System', 'Music', 'Video_editing', 'Firmware', 'casual', 'Games']
    
#     # Fetch registered brands from DB
#     from models.plant_brand import PlantBrand
#     brands = PlantBrand.query.all()

#     return render_template('product_templates/add_product.html', categories=categories, brands=brands)


@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        cost = request.form['cost']
        version = request.form['version']
        description = request.form['description']
        brand_id = request.form['brand_id']

        category_id = request.form.get('category_id')
        custom_category = request.form.get('custom_category')

        if custom_category:  # Add new category if provided
            new_cat = Category(name=custom_category)
            db.session.add(new_cat)
            db.session.commit()
            category_id = new_cat.id

        product = Product(
            name=name,
            cost=cost,
            version=version,
            description=description,
            supplier_id=current_user.id,
            plant_brand_id=brand_id,
            category_id=category_id
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('product.view_products'))

    categories = Category.query.all()
    brands = PlantBrand.query.all()
    return render_template('product_templates/add_product.html', categories=categories, brands=brands)



# @product_bp.route('/<int:product_id>/add_subproduct', methods=['GET', 'POST'])
# @login_required
# def add_subproduct(product_id):
#     if request.method == 'POST':
#         name = request.form['name']
#         version = request.form['version']
#         description = request.form['description']

#         subproduct = SubProduct(name=name, version=version, description=description,
#                                 product_id=product_id, supplier_id=current_user.id)
#         db.session.add(subproduct)
#         db.session.commit()
#         flash('SubProduct added successfully!', 'success')
#         return redirect(url_for('product.product_details', product_id=product_id))
    
#     return render_template('product_templates/add_subproduct.html', product_id=product_id)

@product_bp.route('/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    subproducts = product.subproducts  # Access via relationship
    return render_template('product_templates/product_details.html', product=product, subproducts=subproducts)


@product_bp.route('/add_subproduct', methods=['GET', 'POST'])
@login_required
def add_subproduct():
    from models.product import Product
    if request.method == 'POST':
        name = request.form['name']
        version = request.form['version']
        description = request.form['description']
        product_id = request.form['product_id']

        subproduct = SubProduct(
            name=name,
            version=version,
            description=description,
            product_id=product_id,
            supplier_id=current_user.id
        )
        db.session.add(subproduct)
        db.session.commit()
        flash('SubProduct added successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    products = Product.query.filter_by(supplier_id=current_user.id).all()
    return render_template('product_templates/add_subproduct.html', products=products)
