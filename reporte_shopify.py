import sqlite3
import pandas as pd

try:
    df = pd.read_csv('shopify_trending_products_2025.csv')
except Exception as e:
    print(f'Fallo la lectura bro {e}')


conexion=sqlite3.connect(':memory:')
df.to_sql('shopify_tabla', conexion, index=False, if_exists='replace')

try:
    rendimiento_categoria=''' Select Category, sum(Estimated_Total_Units_Sold_in_2025) as Total_vendido,
        sum(Estimated_Revenue_in_2025_USD) as Ingreso_estimado
    FROM shopify_tabla 
    group by Category;
    '''
except sqlite3.Error as e:
    print(f'Fallo en nuestra base de datos {e}')
rendimiento=pd.read_sql_query( rendimiento_categoria ,conexion)
#print(rendimiento)

try:
    producto_estrella='''SELECT Product_name, sum(Estimated_Total_Units_Sold_in_2025) as Total_por_producto, Category
    FROM shopify_tabla
    group by product_name
    '''
except sqlite3.Error as e:
    print(f'Fallo en nuestra base de datos {e}')
top=pd.read_sql_query(producto_estrella, conexion)
#print(top)


reporte= pd.merge(top, rendimiento, on='Category', how='inner')
reporte= reporte.sort_values(by='Ingreso_estimado', ascending=False)
#con el drop._duplicates(subset=category) estamos borrando los duplicados de esa categoria
reporte=reporte.drop_duplicates(subset=['Category'])

reporte['Total_por_producto'] = reporte['Total_por_producto'].apply(lambda x: f'{x:,} unidades')
reporte['Ingreso_estimado'] = reporte['Ingreso_estimado'].apply(lambda x: f'${x/1e6:.2f} M')
reporte['Total_vendido'] = reporte['Total_vendido'].apply(lambda x: f'{x/1e6:.2f} M unidades')

print(reporte)