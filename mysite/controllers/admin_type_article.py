#! /usr/bin/python
# -*- coding:utf-8 -*-
from mimetypes import types_map
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_meuble ORDER BY type_meuble_libelle ASC;")
    types_meubles = mycursor.fetchall()
    mycursor.execute("SELECT type_meuble.type_meuble_id, COUNT(nom) as nombre_modeles FROM meuble RIGHT JOIN type_meuble ON meuble.type_meuble_id = type_meuble.type_meuble_id GROUP BY type_meuble.type_meuble_id;")
    stocks = mycursor.fetchall()
    return render_template('admin/type_article/show_type_article.html', types_meubles=types_meubles, stocks=stocks)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/valid-add', methods=['POST'])
def valid_add_type_article():
    mycursor = get_db().cursor()
    libelle = request.form.get('libelle')

    mycursor.execute("INSERT INTO type_meuble(type_meuble_libelle) VALUES(%s);", (libelle))
    get_db().commit()
    flash('Ajout d\'un nouveau type meuble : ' + libelle)
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/delete/<int:id>', methods=['GET'])
def delete_type_article(id):
    mycursor = get_db().cursor()

    mycursor.execute("SELECT * FROM type_meuble WHERE type_meuble_id = %s;", (id))
    libelle = mycursor.fetchone()
    libelle = libelle['type_meuble_libelle']

    mycursor.execute("SELECT type_meuble.type_meuble_id, COUNT(meuble.nom) AS nombre FROM meuble RIGHT JOIN type_meuble ON meuble.type_meuble_id = type_meuble.type_meuble_id WHERE type_meuble.type_meuble_id = %s GROUP BY(type_meuble.type_meuble_id)", (id))
    nombre = mycursor.fetchone()
    nombre = nombre['nombre']

    if nombre == 0:

        mycursor.execute("DELETE FROM type_meuble WHERE type_meuble_id = %s;", (id))
        get_db().commit()
        flash('Suppression du type meuble : ' + libelle)
        return redirect('/admin/type-article/show')

    elif nombre > 0:
        mycursor.execute("SELECT * FROM meuble INNER JOIN type_meuble ON meuble.type_meuble_id = type_meuble.type_meuble_id WHERE type_meuble.type_meuble_id = %s ORDER BY meuble.nom;", (id))
        meubles = mycursor.fetchall()

        return render_template('admin/type_article/delete_type_article.html', meubles=meubles, nombre=nombre, libelle=libelle)

@admin_type_article.route('/admin/type-article/meuble-delete/<int:id>', methods=['GET'])
def delete_type_article_meuble(id):
    mycursor = get_db().cursor()

    mycursor.execute("SELECT * FROM meuble WHERE meuble_id = %s;", (id))
    nom = mycursor.fetchone()
    nom = nom['nom']

    mycursor.execute("SELECT * FROM meuble WHERE meuble_id = %s;", (id))
    type_meuble = mycursor.fetchone()
    type_meuble = type_meuble['type_meuble_id']

    mycursor.execute("SELECT * FROM panier WHERE meuble_id = %s;", (id))
    is_in_panier = mycursor.fetchone()
    if is_in_panier:
        mycursor.execute("DELETE FROM panier WHERE meuble_id = %s;", (id))

    mycursor.execute("SELECT * FROM ligne_commande WHERE meuble_id = %s;", (id))
    is_in_ligne_commande = mycursor.fetchone()
    if is_in_ligne_commande:
        mycursor.execute("UPDATE commande SET nbr_articles = nbr_articles - %s, prix_total = prix_total - (%s * %s) WHERE commande_id = %s;", (is_in_ligne_commande['quantite'], is_in_ligne_commande['prix_unit'], is_in_ligne_commande['quantite'], is_in_ligne_commande['commande_id']))
        mycursor.execute("DELETE FROM ligne_commande WHERE meuble_id = %s;", (id))

    mycursor.execute("DELETE FROM meuble WHERE meuble_id = %s;", (id))
    get_db().commit()
    flash('Le meuble : ' + nom + ' a été supprimé')

    mycursor.execute("SELECT type_meuble.type_meuble_id, COUNT(meuble.nom) AS nombre FROM meuble RIGHT JOIN type_meuble ON meuble.type_meuble_id = type_meuble.type_meuble_id WHERE type_meuble.type_meuble_id = %s GROUP BY type_meuble.type_meuble_id;", (type_meuble))
    nombre = mycursor.fetchone()
    nombre = nombre['nombre']
    if nombre == 0:
        return redirect('/admin/type-article/show')

    else:
        id = type_meuble
        return redirect(url_for('admin_type_article.delete_type_article', id=id))

    return render_template('admin/type_article/delete_type_article.html')

@admin_type_article.route('/admin/type-article/edit/<int:id>', methods=['GET'])
def edit_type_article(id):
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_meuble WHERE type_meuble_id = %s;", (id))
    type_meuble = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_meuble=type_meuble)

@admin_type_article.route('/admin/type-article/valid-edit', methods=['POST'])
def valid_edit_type_article():
    mycursor = get_db().cursor()
    id= request.form.get('id')
    libelle = request.form.get('libelle')

    mycursor.execute("UPDATE type_meuble SET type_meuble_libelle = %s WHERE type_meuble_id = %s;", (libelle, id))
    get_db().commit()
    flash('Modification du type meuble : ' + libelle )
    return redirect('/admin/type-article/show') #url_for('show_type_article')

