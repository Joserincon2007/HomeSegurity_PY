#!/bin/bash
echo "🚀 Iniciando despliegue..."
cd /var/www/HomeSegurity_PY
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart homesegurity
sudo systemctl restart nginx
echo "✅ ¡Proyecto actualizado con éxito!"
