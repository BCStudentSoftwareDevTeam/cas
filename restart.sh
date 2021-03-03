echo "WARNING: You need to move this file to the web room (outside of cas-flask) for it to "
echo "work correctly! Failure to do so will result in commands being issued against the "
echo "wrong directory. The commands WILL NOT FAIL!"


cd /var/www/html/
sudo rm -R cas-flask/
cp -R cas-flask-start cas-flask
sudo chown -R cas_dev:www-data cas-flask/
cp ~/room-database\ \(3\).csv ./cas-flask/room-database.csv
cd cas-flask/
git pull origin jamal_basanta
# git rm -f app/config.yaml         # No longer required for secret_config.yaml
# git commit -m "Removing config.yaml for production push"
git checkout jamal_basanta
python update_schema.py
python addClassrooms.py
sudo service apache2 restart
