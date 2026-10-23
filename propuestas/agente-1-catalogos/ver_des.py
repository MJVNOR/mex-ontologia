import re
ttl = open('data/semantica/interpretaciones.ttl', encoding='utf-8').read()
i = ttl.find('a2902c1feb2fa4b8349946c2ae418a11bf0f465032c5c62adaf33fb053373cf2')
print(ttl[max(0,i-500):i+2500])
