import boto3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ec2 = boto3.resource("ec2")

custom_filter = [
    {
        "Name": "tag:Environment",
        "Values": ["Dev"]
    }
]

# --- 1. MALZEMECİ ---
def sunuculari_bul():
    """AWS'ye gidip listeyi alıp getiren fonksiyon"""
    logging.info("Sunucular Aranıyor...")
    
    target_instances = ec2.instances.filter(Filters=custom_filter)
    return target_instances

# --- 2. GECE AMİRİ ---
def gece_operasyonu(gelen_liste): 
    # ATTENTION: We build the cycle on the "incoming_list" from the parentheses.
    for sunucu in gelen_liste:
        logging.info(f"İncelenen ID: {sunucu.id} - Durum: {sunucu.state['Name']}")
        
        if sunucu.state["Name"] == "running":
            try:
                logging.info(f"{sunucu.id} durduruluyor...")
                sunucu.stop() # Tetik
                sunucu.wait_until_stopped() # Bekleme (stopped)
                logging.info(f"BAŞARILI: {sunucu.id} durduruldu.")
            except Exception as e:
                logging.error(f"Hata: {e}")
        elif sunucu.state['Name'] == "stopped":
            logging.info(f"{sunucu.id} zaten durmuş, işlem yapılmadı.")

# --- 3. SABAH AMİRİ ---
def sabah_operasyonu(gelen_liste):
    for instance in gelen_liste:
        logging.info(f"İncelenen ID: {instance.id} - Durum: {instance.state['Name']}")
        
        if instance.state['Name'] == "stopped":
            try:
                logging.info(f"{instance.id} başlatılıyor...")
                instance.start() 
                instance.wait_until_running() # Bekleme
                logging.info(f"BAŞARILI: {instance.id} çalışıyor.") # DÜZELTME: logging.info
            except Exception as e:
                logging.error(f"Hata: {e}")
        elif instance.state['Name'] == "running":
            logging.info(f"{instance.id} zaten çalışıyor.")

# --- 4. KOMUTA CENTER (Main Block) ---
#  This is where we call the functions.

if __name__ == "__main__":
    # take the list
    bulunan_sunucular = sunuculari_bul()
    
    secim = input("Hangi Operasyon? (1: Gece/Kapat, 2: Sabah/Aç): ")
    
    if secim == "1":
        # We deliver the list to the night manager
        gece_operasyonu(bulunan_sunucular)
    elif secim == "2":
        # We deliver the list to the morning supervisor
        sabah_operasyonu(bulunan_sunucular)
    else:
        print("Geçersiz seçim.")
