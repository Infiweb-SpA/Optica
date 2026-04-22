from flask import Flask, render_template, request
from models import db, Product, Announcement
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///optic_clarity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------- Rutas ----------
@app.route('/')
def index():
    """Landing page principal."""
    featured_frames = Product.query.filter_by(type='frame').limit(3).all()
    return render_template('index.html', featured_frames=featured_frames)

@app.route('/catalogo')
def catalog():
    """Catálogo de marcos y lentes con filtros."""
    # Obtener parámetros de filtro (opcional)
    type_filter = request.args.get('type', 'all')  # 'frame', 'lens', 'all'
    style_filter = request.args.get('style', '')
    material_filter = request.args.get('material', '')
    
    query = Product.query
    if type_filter != 'all':
        query = query.filter_by(type=type_filter)
    if style_filter:
        query = query.filter_by(style=style_filter)
    if material_filter:
        query = query.filter_by(material=material_filter)
    
    products = query.all()
    # Contar estilos y materiales para los filtros (puedes obtenerlos de la DB)
    styles = db.session.query(Product.style).distinct().all()
    materials = db.session.query(Product.material).distinct().all()
    
    return render_template('catalog.html', 
                           products=products,
                           type_filter=type_filter,
                           styles=[s[0] for s in styles if s[0]],
                           materials=[m[0] for m in materials if m[0]])

@app.route('/eventos')
def events():
    """Página de operativos y anuncios."""
    today = date.today()
    upcoming = Announcement.query.filter(Announcement.event_date >= today, Announcement.is_past == False).order_by(Announcement.event_date).all()
    past = Announcement.query.filter((Announcement.event_date < today) | (Announcement.is_past == True)).order_by(Announcement.event_date.desc()).limit(3).all()
    featured = Announcement.query.filter_by(is_featured=True).first()
    return render_template('events.html', 
                           upcoming=upcoming, 
                           past=past,
                           featured=featured)

@app.route('/contacto')
def contact():
    """Página de ubicación y contacto."""
    return render_template('contact.html')

# ---------- Comando CLI para inicializar datos de ejemplo ----------
@app.cli.command('init-db')
def init_db_command():
    """Crea las tablas y carga datos de demostración."""
    db.create_all()
    
    # Marcos de ejemplo
    frames = [
        Product(type='frame', name='Aero Classic', brand='VOGUE OPTICS', price=285.00,
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuCOo5oxuaFSeJh695485oN5jMcHYrw5Q9Yu8nEMwqp9APlfcInxcQ-DLbVgr1ZGTW_cSrunhlvOY73nIz2rIoUFIl92olJKqNN00noU6OC7Mj1fK8FQGnHCrdq_iG-k3ZHtpztk_oY3bXIRx_b4pABNCa_9XLLd5YW9lKlJqxOTXk-A6ToH1FBFxtle6EZnXcu37kog8RbzQV6kTAiaEAGhwLMHXtkqNZ4UpRdiwauXI9x_hQtxyRVKY8qAsx7LJgWc3ey9hPj_30c',
                color='Negro', material='Acetato', style='Moderno'),
        Product(type='frame', name='Orbital Gold', brand='TITAN SERIES', price=420.00,
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuDrhRW7WA0jApG5YIoOK3swqZlU8btPZJM41NRgMqboUB_kVAIEiC2cXP9C1QeVwmNVNFsrOOwpW4TlfLoMV-I6XQZruijfg_JlecSd8D9lfIqJlzUB_aLUkO_lOGYZAdDl0k85qxuqetCW4EkhFaTTseliptDHAodVAD-a2bIPjtnHu-KUIlfzl2ar0J2NMATmeKzkEzjdth3eTeR0nUSRd_3ZR4jsWgAnSse3jEZNvu2ICEyg_CZ7EXxllW_eQLSGvm5ERa21TII',
                color='Dorado', material='Titanio', style='Clásico'),
        Product(type='frame', name='Vienna Shell', brand='NOUVEAU RITUAL', price=315.00,
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuAryHzkLtg027d4ixTNgvv7vQjaCOcGQZCgrZdlYD_WOyiUVx-bdpB-WP-wnaj8dJzb7uq-yCQlTe706GoxK8jD_HWV2zMtaU95piUbhVR9KWzZdTsOBYHE1djcaMTSMivm55xZP2u9Us8UvZKeUT6wLJrSaFbyzkG7HDOCpQOIruBJYv5d6QaTTAo43E4kb6dRW-_4-bjklUEjmPy-O8x_4_hz-wcqxhups70V1zN1MrYmY5czUm_9qdedyq0NZvx-Vno3bTAaokY',
                color='Carey', material='Acetato', style='Retro'),
        Product(type='frame', name='Azure Frost', brand='MODERNIST', price=260.00,
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuBLjef1tva6RSklzeCvfrWnf9aLhiIYnXFdF6Jlz-qPObjB9AYKGcYbeVSdk2Vaml9wjn6cl48gk9HApx0g3-HxMymG0cr5-S59pch8VgSYunhZT1hSL5coJMcqnb7glLwTkLZTt0T0bINYfZLcHJp_XvC2-sqByGErXlFz_RoZ4nuvb2htg30F7K7LGDxNg6UML2bYALTfXY_d1-r2Iu14f0IWYNBPQGIkDSrf_sQyMIUPs2XBTZz-5_l8S62F8WQIOfWVxBewSwg',
                color='Azul', material='Acetato', style='Moderno'),
        Product(type='frame', name='Pilot Prime', brand='HERITAGE', price=390.00,
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuAX4rxgYqInT4uiPdF3qE6_KrJ3frGQuTmXO9oG-1eEDKBn5cqVVPsbFVWmUytMj4vA2qiHlypZ4Ljf_QyBBJxvBo255Ogl8OkIpDbIDQyp5af0RqqSx90r3xa5dSIk4jLTjjqBU1KWwtKEGzwKQ54WVCcbUWXDJ_aNJd1iqNeyWN4TOSLaCu9wDkzMiWkLe3e_hR7OEgcKJIZTJtY3SrQqYc7M0CczwGePK29ARYjFM8QzQWapK8aGhaEQBbD_EW7tD8cl0oeevbs',
                color='Plata', material='Metal', style='Aviador'),
        Product(type='frame', name='Bento Block', brand='URBAN ARCHITECT', price=340.00,
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuDidA2txONkpzwZXAZh-nAO3khgdmmC8ec4LsMD9AzxFQlUtjIw0VuYuWowCwvqlwVTc0rzeYigRoqVU0x1KcQeTIMzZMKnLuO9vGrJoFnA6yJBLdvYh9CY7ynwnJqRqQ5IWUyE_CMoFtL6NWkkrYBY6cmifqEQTl2-Yw6pW_EG6x5xp9EPDFRtHhKoVLaZrzqGkaoTz7ShIR9aL-3hOKPl1r5kEH3CVMuPRmceCv4rirWW_3QyOK5w5wm91Ekj2rdhTCi2zy3SqjY',
                color='Negro', material='Acetato', style='Moderno'),
    ]
    
    # Lentes de ejemplo
    lenses = [
        Product(type='lens', name='Digital HD Clear', brand='OpticClarity Lab', price=180.00,
                description='Lentes personalizados con filtro de luz azul y anti-reflejo.',
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuA_3T-M9mbyXkkRkLVQg3yf1sDPZu16pWkpO9s6nNXf7nXY3t0WUi821QcdxNsOuv2nZbXp1UcxVR9EwJ4_LuqQLpO1waiqOaN8UGT3wPfB-XHq3XdAdnPinae8CR_ZPulT5hAExtt1A7WibN4rsLj3YuEbdTxFzjnobVcvXO5rdVgFf-S3sy0Z2f8t6ZmgGkflE9liiLutle_WTo3U5t7wTWee32VnZ7ZFytfEAoZwq_FghLdONNjBlmLqj0QNWkyYBY4_tvOt4xM',
                features='Blue Light, Anti-reflejo', material='Policarbonato'),
        Product(type='lens', name='Progressive Elite', brand='OpticClarity Lab', price=320.00,
                description='Lentes progresivos de última generación con transición suave.',
                image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuA_3T-M9mbyXkkRkLVQg3yf1sDPZu16pWkpO9s6nNXf7nXY3t0WUi821QcdxNsOuv2nZbXp1UcxVR9EwJ4_LuqQLpO1waiqOaN8UGT3wPfB-XHq3XdAdnPinae8CR_ZPulT5hAExtt1A7WibN4rsLj3YuEbdTxFzjnobVcvXO5rdVgFf-S3sy0Z2f8t6ZmgGkflE9liiLutle_WTo3U5t7wTWee32VnZ7ZFytfEAoZwq_FghLdONNjBlmLqj0QNWkyYBY4_tvOt4xM',
                features='Progresivo, Fotocromático', material='Alto índice')
    ]
    
    db.session.add_all(frames + lenses)
    
    # Anuncios/Operativos
    announcements = [
        Announcement(title='Operativo de Visión 2024', 
                     description='Jornada comunitaria de salud visual en San José.',
                     event_date=date(2024, 10, 14), location='San Jose Community Center',
                     image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuB-2sBaY7SPF2tbfeVrL03ef8qJbnnidMaDJQr5FEeL8_GF16fhTEhtsPEF1uV3qCozlOWzaZ14g0uHTxxyN3ALd3iPBnRrsfRojYXS2yF0cWvGXzv4Al8wiuuYt6-BAmEym7tmBSyFl2pU4MkvNOrZLlb6pM8mJUW088ZfX__3yUQENlokP2hlGPzMhZRIyhuvTVWT7ztigdI52VJdLm79YRjUG-kzPx5OuL8E3McaLnLsFru9nGcEn5KeX7ifx6X5zx7YQTV8Q4o',
                     is_featured=True),
        Announcement(title="Children's Vision Month Launch",
                     event_date=date(2024, 11, 5), location='OpticClarity Main Studio',
                     image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuBp9jvt1_UxJ2yGFS6wGC_rb7eJ7wrhkoAWc_KfhrGk8bW0lUc_0ZmIhG-98wB1I430E4T7lf-V7n55X8ObtsWAdgLzcRUPeKkkShuCtFbnhuxeBBICdyFiAHhna5VNtCqOVHKKiBANXpyrlAPMu4QZNA5Yjm1gc134wg_SoJp77iKdBfzRqOq46yE62Ibv3g8rV_FCG_gg1QYN6CIJOCUNnICqQxDJd8K6FkXTWFmU-2gR2UI-O0oqBhTQrQQmoUlCcsyekVFwXrM'),
        Announcement(title='Glaucoma Screening Awareness',
                     event_date=date(2024, 11, 18), location='OpticClarity Main Studio',
                     image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuA_3T-M9mbyXkkRkLVQg3yf1sDPZu16pWkpO9s6nNXf7nXY3t0WUi821QcdxNsOuv2nZbXp1UcxVR9EwJ4_LuqQLpO1waiqOaN8UGT3wPfB-XHq3XdAdnPinae8CR_ZPulT5hAExtt1A7WibN4rsLj3YuEbdTxFzjnobVcvXO5rdVgFf-S3sy0Z2f8t6ZmgGkflE9liiLutle_WTo3U5t7wTWee32VnZ7ZFytfEAoZwq_FghLdONNjBlmLqj0QNWkyYBY4_tvOt4xM'),
        Announcement(title='Annual Santa Clara Operativo',
                     event_date=date(2024, 9, 22), location='Santa Clara Community Hall',
                     image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuBVSk3oF90j06FTu3V_VRS09uw3S0K8JDGFNQ6vlNBa30ZpexbxLDN3v_CF3Gr-qI03dolMQh-L4erLEYxQvoEIvHlbofv7aNHuPSkSIv_fwFqDgrP3r5gqJ6yeAMT7YT4w1W5P49iLX5fJBjbsPcLl1k97SMlC_W5MkaawYel0rtp2VoCMwI9mH-hfe17bUST5yeQBWXWDQCna6z3ZZtx2RodSu67HEuoPV00A--FIOxi04f82BTSnJBQ77k89mNNwWfJpJZ-XXu8',
                     is_past=True)
    ]
    db.session.add_all(announcements)
    db.session.commit()
    print('Base de datos inicializada con datos de ejemplo.')

if __name__ == '__main__':
    app.run(debug=False,  host='0.0.0.0', port=8080)
