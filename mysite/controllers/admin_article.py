#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                        template_folder='templates')

@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM meuble INNER JOIN type_meuble ON meuble.type_meuble_id = type_meuble.type_meuble_id INNER JOIN marque ON meuble.marque_id = marque.marque_id ORDER BY type_meuble.type_meuble_libelle ASC;")
    meubles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', meubles=meubles)

@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM type_meuble ORDER BY type_meuble_libelle;")
    types_meubles = mycursor.fetchall()
    mycursor.execute("SELECT * FROM marque ORDER BY marque_libelle;")
    marques = mycursor.fetchall()
    return render_template('admin/article/add_article.html', types_meubles=types_meubles, marques=marques)

@admin_article.route('/admin/article/valid-add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    prix = request.form.get('prix')
    type_meuble = request.form.get('type_meuble')
    marque = request.form.get('marque')
    stock = request.form.get('stock')

    mycursor.execute("INSERT INTO meuble(nom, prix_unit, marque_id, stock, type_meuble_id) VALUE(%s, %s, %s, %s, %s);", (nom, prix, marque, stock, type_meuble))
    get_db().commit()

    mycursor.execute("SELECT * FROM type_meuble WHERE type_meuble_id = %s;", (type_meuble))
    type_meuble = mycursor.fetchone()
    type_meuble = type_meuble['type_meuble_libelle']

    mycursor.execute("SELECT * FROM marque WHERE marque_id = %s;", (marque))
    marque = mycursor.fetchone()
    marque = marque['marque_libelle']

    flash('Ajout d\'un nouveau meuble : ' + nom + ' -- prix : ' + prix + ' € -- marque : ' + marque + ' -- stock : ' + stock + ' -- libellé : ' + type_meuble)
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/delete/<int:id>', methods=['GET'])
def delete_article(id):
    mycursor = get_db().cursor()

    mycursor.execute("SELECT * FROM meuble WHERE meuble_id = %s;", (id))
    nom = mycursor.fetchone()
    nom = nom['nom']

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

    print("un article supprimé, id :", id)
    flash(u'Le meuble ' + nom + ' a été supprimé')
    return redirect(url_for('admin_article.show_article'))

@admin_article.route('/admin/article/edit/<int:id>', methods=['GET'])
def edit_article(id):
    mycursor = get_db().cursor()
    mycursor.execute("SELECT * FROM meuble INNER JOIN type_meuble ON meuble.type_meuble_id = type_meuble.type_meuble_id INNER JOIN marque ON meuble.marque_id = marque.marque_id WHERE meuble_id = %s ORDER BY type_meuble.type_meuble_libelle ASC;", (id))
    meuble = mycursor.fetchone()
    mycursor.execute("SELECT * FROM type_meuble ORDER BY type_meuble_libelle;")
    types_meubles = mycursor.fetchall()
    mycursor.execute("SELECT * FROM marque ORDER BY marque_libelle;")
    marques = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', meuble=meuble, types_meubles=types_meubles, marques=marques)

@admin_article.route('/admin/article/valid-edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    id = request.form.get('id')
    nom = request.form.get('nom')
    prix = request.form.get('prix')
    type_meuble = request.form.get('type_meuble')
    marque = request.form.get('marque')
    stock = request.form.get('stock')

    mycursor.execute("UPDATE meuble SET nom = %s, prix_unit = %s, marque_id = %s, stock = %s, type_meuble_id = %s WHERE meuble_id = %s;", (nom, prix, marque, stock, type_meuble, id))
    get_db().commit()

    mycursor.execute("SELECT * FROM type_meuble WHERE type_meuble_id = %s;", (type_meuble))
    type_meuble = mycursor.fetchone()
    type_meuble = type_meuble['type_meuble_libelle']

    mycursor.execute("SELECT * FROM marque WHERE marque_id = %s;", (marque))
    marque = mycursor.fetchone()
    marque = marque['marque_libelle']

    flash('Modification du meuble : ' + nom + ' -- prix : ' + prix + ' € -- marque : ' + marque + ' -- stock : ' + stock + ' -- libellé : ' + type_meuble)
    return redirect(url_for('admin_article.show_article'))
    return redirect(url_for('admin_article.show_article'))

