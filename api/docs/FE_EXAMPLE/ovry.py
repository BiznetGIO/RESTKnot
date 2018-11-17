data = 'a:3:{s:8:"user_ref";i:344509;s:8:"site_ref";i:336027;s:11:"package_ref";s:4:"2563";}'

data = data.split("site_ref")
site_ref = data[1]
data = data[0]
data = data.split("user_ref")
data = data[1]
data = data.split(";")
print(data[1])
