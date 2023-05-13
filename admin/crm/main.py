from flaskblog import app

if __name__ == '__main__':
    app.run(debug=True)




# with app.app_context():
#     db.session.query(User).delete()
#     db.session.commit()

#     user_1 = User(username='Martin', email='martinpellizzer@gmail.com', password='Newoliark1')
#     db.session.add(user_1)
#     user_2 = User(username='Elena', email='elenaceccato@gmail.com', password='Asia123')
#     db.session.add(user_2)
#     db.session.commit()

# with app.app_context():
#     user = User.query.first()
#     post_1 = Post(title='Blog 1', content='first post content', user_id=user.id)
#     post_2 = Post(title='Blog 2', content='second post content', user_id=user.id)
#     db.session.add(post_1)
#     db.session.add(post_2)
#     db.session.commit()
    
# with app.app_context():
#     user = User.query.first()
#     print(user.posts)

# with app.app_context():
#     db.drop_all()
#     db.create_all()



