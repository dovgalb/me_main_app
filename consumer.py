import json
from main import Product, db
import pika

params = pika.URLParameters(
    'amqps://gjbweibk:eL88hOkPdDTTII1I8d7mtO6nTGZscunX@cow.rmq2.cloudamqp.com/gjbweibk'
)

connection = pika.BlockingConnection(params)

chanel = connection.channel()

chanel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('product updated')


    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('product deleted')

chanel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('started consuming')

chanel.start_consuming()

chanel.close()
