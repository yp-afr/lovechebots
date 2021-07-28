from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import func

from . import db
from .models import AfficheNames, AfficheSubcategories, AfficheCategories, AfficheRecords, FindsNames
from .scripts.load_cats_subcats import get_categories, get_subcategories_by_category_code
from .scripts.load_info_about_clicks import get_clicks
from .scripts.load_info_about_creating_posts import get_creating_posts_stats
from .scripts.load_info_about_new_users import get_new_users_info_affiche, get_new_users_info_finds
from .scripts.load_info_about_subscriptions import get_subscriptions
from .scripts.load_info_about_unsubscribe import get_unsubscribe
from .scripts.load_names import get_names_affiche, get_names_finds

views = Blueprint('views', __name__)


@views.route('/bots')
@login_required
def bots():
    return render_template('bots.html')


@views.route('/bots/finds')
@login_required
def finds():
    return 'Finds Dashboard'


@views.route('/bots/affiche/statistics')
@login_required
def affiche_stats():
    row1, rows7, rows30, rows_count = get_new_users_info_affiche()
    return render_template('affiche_statistics.html', data1=row1, data7=rows7, data30=rows30,
                           rows_count=rows_count)


@views.route('/get_stats/', methods=['GET', 'POST'])
def get_stats():
    result = get_clicks()
    for_clicks_chart = {}
    for_clicks_chart["jsonarray"] = []
    for category, subcategory, count in result:
        for_clicks_chart[subcategory] = count
        temp_d = {}
        temp_d["cat"] = category
        temp_d["c"] = count
        temp_d["sub"] = subcategory

        for_clicks_chart["jsonarray"].append(temp_d)

    return jsonify(for_clicks_chart)


@views.route('/get_subscriptions_stats/', methods=['GET', 'POST'])
def get_subscriptions_stats():
    val = {}
    wth_categories, wth_subcategories = get_subscriptions()
    val['wth_cats'] = wth_categories
    val['wth_subcats'] = wth_subcategories
    return jsonify(val)


@views.route('/get_unsubscribe_stats/', methods=['GET', 'POST'])
def get_unsubscribe_stats():
    val = {}
    wth_categories, wth_subcategories = get_unsubscribe()
    val['wth_cats'] = wth_categories
    val['wth_subcats'] = wth_subcategories
    return jsonify(val)


@views.route('/bots/affiche/db')
@login_required
def affiche_db():
    names = get_names_affiche()
    cat_subcat = {}
    categories = get_categories()
    for category in categories:
        tpl = (category.category_name, category.category_code)
        cat_subcat[tpl] = get_subcategories_by_category_code(category.category_code)
    return render_template('affiche_db.html', names=names, cat_subcat=cat_subcat)


@views.route('/bots/affiche/db/edit_name/<int:name_id>', methods=['GET', 'POST'])
@login_required
def edit_name(name_id):
    if request.method == 'POST':
        nid = request.form.get('nameID')
        try:
            new_value = request.form.get('newvalue')
            name_row = AfficheNames.query.get(nid)
            name_row.value = new_value
            print(name_row)
            db.session.commit()
            flash("Успешно изменено!", 'success')
            return redirect(url_for('views.affiche_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка изменения!", 'error')
    name = AfficheNames.query.get_or_404(int(name_id))
    return render_template('edit_name.html', name=name)


@views.route('/bots/affiche/db/addsubcategory', methods=['GET', 'POST'])
@login_required
def add_subcategory():
    if request.method == 'POST':
        cid = request.form.get('id_category')
        sname = request.form.get('subcategory_name')
        scode = request.form.get('subcategory_code')
        try:
            res = db.session.query(func.count(AfficheSubcategories.id)).filter(
                AfficheSubcategories.category_code == cid).scalar()
            if res == 0:
                current_category = AfficheCategories.query.filter_by(category_code=cid).first()
                current_category.is_subcategories = True
            new_subcat = AfficheSubcategories()
            new_subcat.subcategory_name = sname
            new_subcat.subcategory_code = scode
            new_subcat.category_code = cid
            db.session.add(new_subcat)
            db.session.commit()
            flash("Успешно добавлено!", 'success')
            return redirect(url_for('views.affiche_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка добавления!", 'error')
            return redirect(url_for('views.affiche_db'))


@views.route('/bots/affiche/db/deletesubcategory', methods=['GET', 'POST'])
@login_required
def del_subcategory():
    if request.method == 'POST':
        sid = request.form.get('id_del_sub')
        cid = request.form.get('id_del_sub_cat_code')
        try:
            deleting_subcat = AfficheSubcategories.query.filter_by(subcategory_code=sid).first()
            db.session.delete(deleting_subcat)
            AfficheRecords.query.filter_by(subcategory_name=sid).delete()
            db.session.commit()
            flash("Успешно удалено!", 'success')
            res = db.session.query(func.count(AfficheSubcategories.id)).filter(
                AfficheSubcategories.category_code == cid).scalar()
            if res == 0:
                current_category = AfficheCategories.query.filter_by(category_code=cid).first()
                current_category.is_subcategories = False
                db.session.commit()
            return redirect(url_for('views.affiche_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка удаления!", 'error')
            return redirect(url_for('views.affiche_db'))


@views.route("/bots/affiche/db/add-category", methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        cat_code = request.form.get('category_code')
        cat_name = request.form.get('category_name')
        try:
            cat = AfficheCategories()
            cat.category_name = cat_name
            cat.category_code = cat_code
            cat.is_subcategories = False
            db.session.add(cat)
            db.session.commit()
            flash("Успешно добавлено!", 'success')
            return redirect(url_for('views.affiche_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка добавления!", 'error')
            return redirect(url_for('views.affiche_db'))


@views.route('/bots/affiche/db/del-category', methods=['GET', 'POST'])
@login_required
def del_category():
    if request.method == 'POST':
        cid = request.form.get('id_deleting_category')
        try:
            deleting_cat = AfficheCategories.query.filter_by(category_code=cid).first()
            db.session.delete(deleting_cat)
            AfficheSubcategories.query.filter_by(category_code=cid).delete()
            AfficheRecords.query.filter_by(category_name=cid).delete()
            db.session.commit()
            flash("Успешно удалено!", 'success')
            return redirect(url_for('views.affiche_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка удаления!", 'error')
            return redirect(url_for('views.affiche_db'))


@views.route('/bots/affiche/db/edit-subcategory', methods=['GET', 'POST'])
@login_required
def edit_subcategory():
    if request.method == 'POST':
        new_name = request.form.get('new_subcategory_name')
        code = request.form.get('id_editing_subcategory')
        try:
            sub_row = AfficheSubcategories.query.filter_by(subcategory_code=code).first()
            sub_row.subcategory_name = new_name
            db.session.commit()
            flash("Успешно изменено!", 'success')
            return redirect(url_for('views.affiche_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка изменения!", 'error')
            return redirect(url_for('views.affiche_db'))


@views.route('/bots/affiche/db/edit-category', methods=['GET', 'POST'])
@login_required
def edit_category():
    if request.method == 'POST':
        new_name = request.form.get('new_category_name')
        code = request.form.get('id_editing_category')
        try:
            sub_row = AfficheCategories.query.filter_by(category_code=code).first()
            sub_row.category_name = new_name
            db.session.commit()
            flash("Успешно изменено!", 'success')
            return redirect(url_for('views.affiche_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка изменения!", 'error')
            return redirect(url_for('views.affiche_db'))


@views.route('/bots/finds/db')
@login_required
def finds_db():
    names = get_names_finds()
    return render_template('finds_db.html', names=names)


@views.route('/bots/finds/db/edit_name/<int:name_id>', methods=['GET', 'POST'])
@login_required
def edit_name_finds(name_id):
    if request.method == 'POST':
        nid = request.form.get('nameID')
        try:
            new_value = request.form.get('newvalue')
            name_row = FindsNames.query.get(nid)
            name_row.value = new_value
            print(name_row)
            db.session.commit()
            flash("Успешно изменено!", 'success')
            return redirect(url_for('views.finds_db'))
        except Exception as ex:
            print(ex)
            flash("Ошибка изменения!", 'error')
    name = FindsNames.query.get_or_404(int(name_id))
    return render_template('edit_name_finds.html', name=name)


@views.route('/bots/finds/statistics')
@login_required
def finds_stats():
    row1, rows7, rows30, rows_count = get_new_users_info_finds()
    posting_stats = get_creating_posts_stats()
    return render_template('finds_statistics.html', data1=row1, data7=rows7, data30=rows30,
                           rows_count=rows_count, posting_stats=posting_stats)