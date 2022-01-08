# rails1 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails1.move(z=0.1, x=-6.5, y=-7)
# rails1.rotate(z=180)
# rails1.flip()

# rails2 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails2.move(z=0.1, x=0.5)
# rails2.rotate(z=90)

# rails3 = grid.add_rails(RAILS_RECHT)
# rails3.move(z=0.1, x=0.5)
# rails3.rotate(z=90)

# rails4 = grid.add_rails(RAILS_RECHT)
# rails4.move(z=0.1, x=0.5, y=4)
# rails4.rotate(z=90)

# rails5 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails5.move(z=0.1, x=0.5, y=4)
# rails5.rotate(z=270)
# rails5.flip()

# rails6 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails6.move(z=0.1, x=-6.5, y=11)
# rails6.rotate(z=180)

# rails7 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails7.move(z=0.1, x=-2.5, y=11)
# rails7.flip()

# rails8 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails8.move(z=0.1, x=-9.5, y=4)
# rails8.rotate(z=270)

# rails9 = grid.add_rails(RAILS_RECHT)
# rails9.move(z=0.1, x=-9.5, y=4)
# rails9.rotate(z=90)

# rails10 = grid.add_rails(RAILS_RECHT)
# rails10.move(z=0.1, x=-9.5, y=0)
# rails10.rotate(z=90)

# rails11 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails11.move(z=0.1, x=-9.5)
# rails11.rotate(z=90)
# rails11.flip()

# rails12 = grid.add_rails(RAILS_BOCHT, angle=45)
# rails12.move(z=0.1, x=-2.5, y=-7)

rails1 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=0)
rails1.move(x=-6.5, y=-7)

rails2 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=45)
rails2.move(x=0.5)

rails3 = grid.add_rails(RAILS_RECHT)
rails3.move(x=0.5)
rails3.rotate(90)

rails4 = grid.add_rails(RAILS_RECHT)
rails4.move(x=0.5, y=4)
rails4.rotate(90)

rails5 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=90)
rails5.move(x=0.5, y=4)

rails6 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=135)
rails6.move(x=-6.5, y=11)

rails7 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=180)
rails7.move(x=-2.5, y=11)
rails7.flip()

rails8 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=225)
rails8.move(x=-9.5, y=4)

rails9 = grid.add_rails(RAILS_RECHT)
rails9.move(x=-9.5, y=4)
rails9.rotate(90)

rails10 = grid.add_rails(RAILS_RECHT)
rails10.move(x=-9.5, y=0)
rails10.rotate(90)

rails11 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=270)
rails11.move(x=-9.5)

rails12 = grid.add_rails(RAILS_BOCHT, angle=45, rotation=315)
rails12.move(x=-2.5, y=-7)
