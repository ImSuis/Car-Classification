import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

# Define the number of classes (update this based on your dataset)
num_classes = 196

# Define car labels dictionary (for demonstration purposes)
car_labels_dict = {'AM General Hummer SUV 2000': 0, 'Acura Integra Type R 2001': 1, 'Acura RL Sedan 2012': 2, 'Acura TL Sedan 2012': 3, 'Acura TL Type-S 2008': 4, 'Acura TSX Sedan 2012': 5, 'Acura ZDX Hatchback 2012': 6, 'Aston Martin V8 Vantage Convertible 2012': 7, 'Aston Martin V8 Vantage Coupe 2012': 8, 'Aston Martin Virage Convertible 2012': 9, 'Aston Martin Virage Coupe 2012': 10, 'Audi 100 Sedan 1994': 11, 'Audi 100 Wagon 1994': 12, 'Audi A5 Coupe 2012': 13, 'Audi R8 Coupe 2012': 14, 'Audi RS 4 Convertible 2008': 15, 'Audi S4 Sedan 2007': 16, 'Audi S4 Sedan 2012': 17, 'Audi S5 Convertible 2012': 18, 'Audi S5 Coupe 2012': 19, 'Audi S6 Sedan 2011': 20, 'Audi TT Hatchback 2011': 21, 'Audi TT RS Coupe 2012': 22, 'Audi TTS Coupe 2012': 23, 'Audi V8 Sedan 1994': 24, 'BMW 1 Series Convertible 2012': 25, 'BMW 1 Series Coupe 2012': 26, 'BMW 3 Series Sedan 2012': 27, 'BMW 3 Series Wagon 2012': 28, 'BMW 6 Series Convertible 2007': 29, 'BMW ActiveHybrid 5 Sedan 2012': 30, 'BMW M3 Coupe 2012': 31, 'BMW M5 Sedan 2010': 32, 'BMW M6 Convertible 2010': 33, 'BMW X3 SUV 2012': 34, 'BMW X5 SUV 2007': 35, 'BMW X6 SUV 2012': 36, 'BMW Z4 Convertible 2012': 37, 'Bentley Arnage Sedan 2009': 38, 'Bentley Continental Flying Spur Sedan 2007': 39, 'Bentley Continental GT Coupe 2007': 40, 'Bentley Continental GT Coupe 2012': 41, 'Bentley Continental Supersports Conv. Convertible 2012': 42, 'Bentley Mulsanne Sedan 2011': 43, 'Bugatti Veyron 16.4 Convertible 2009': 44, 'Bugatti Veyron 16.4 Coupe 2009': 45, 'Buick Enclave SUV 2012': 46, 'Buick Rainier SUV 2007': 47, 'Buick Regal GS 2012': 48, 'Buick Verano Sedan 2012': 49, 'Cadillac CTS-V Sedan 2012': 50, 'Cadillac Escalade EXT Crew Cab 2007': 51, 'Cadillac SRX SUV 2012': 52, 'Chevrolet Avalanche Crew Cab 2012': 53, 'Chevrolet Camaro Convertible 2012': 54, 'Chevrolet Cobalt SS 2010': 55, 'Chevrolet Corvette Convertible 2012': 56, 'Chevrolet Corvette Ron Fellows Edition Z06 2007': 57, 'Chevrolet Corvette ZR1 2012': 58, 'Chevrolet Express Cargo Van 2007': 59, 'Chevrolet Express Van 2007': 60, 'Chevrolet HHR SS 2010': 61, 'Chevrolet Impala Sedan 2007': 62, 'Chevrolet Malibu Hybrid Sedan 2010': 63, 'Chevrolet Malibu Sedan 2007': 64, 'Chevrolet Monte Carlo Coupe 2007': 65, 'Chevrolet Silverado 1500 Classic Extended Cab 2007': 66, 'Chevrolet Silverado 1500 Extended Cab 2012': 67, 'Chevrolet Silverado 1500 Hybrid Crew Cab 2012': 68, 'Chevrolet Silverado 1500 Regular Cab 2012': 69, 'Chevrolet Silverado 2500HD Regular Cab 2012': 70, 'Chevrolet Sonic Sedan 2012': 71, 'Chevrolet Tahoe Hybrid SUV 2012': 72, 'Chevrolet TrailBlazer SS 2009': 73, 'Chevrolet Traverse SUV 2012': 74, 'Chrysler 300 SRT-8 2010': 75, 'Chrysler Aspen SUV 2009': 76, 'Chrysler Crossfire Convertible 2008': 77, 'Chrysler PT Cruiser Convertible 2008': 78, 'Chrysler Sebring Convertible 2010': 79, 'Chrysler Town and Country Minivan 2012': 80, 'Daewoo Nubira Wagon 2002': 81, 'Dodge Caliber Wagon 2007': 82, 'Dodge Caliber Wagon 2012': 83, 'Dodge Caravan Minivan 1997': 84, 'Dodge Challenger SRT8 2011': 85, 'Dodge Charger SRT-8 2009': 86, 'Dodge Charger Sedan 2012': 87, 'Dodge Dakota Club Cab 2007': 88, 'Dodge Dakota Crew Cab 2010': 89, 'Dodge Durango SUV 2007': 90, 'Dodge Durango SUV 2012': 91, 'Dodge Journey SUV 2012': 92, 'Dodge Magnum Wagon 2008': 93, 'Dodge Ram Pickup 3500 Crew Cab 2010': 94, 'Dodge Ram Pickup 3500 Quad Cab 2009': 95, 'Dodge Sprinter Cargo Van 2009': 96, 'Eagle Talon Hatchback 1998': 97, 'FIAT 500 Abarth 2012': 98, 'FIAT 500 Convertible 2012': 99, 'Ferrari 458 Italia Convertible 2012': 100, 'Ferrari 458 Italia Coupe 2012': 101, 'Ferrari California Convertible 2012': 102, 'Ferrari FF Coupe 2012': 103, 'Fisker Karma Sedan 2012': 104, 'Ford E-Series Wagon Van 2012': 105, 'Ford Edge SUV 2012': 106, 'Ford Expedition EL SUV 2009': 107, 'Ford F-150 Regular Cab 2007': 108, 'Ford F-150 Regular Cab 2012': 109, 'Ford F-450 Super Duty Crew Cab 2012': 110, 'Ford Fiesta Sedan 2012': 111, 'Ford Focus Sedan 2007': 112, 'Ford Freestar Minivan 2007': 113, 'Ford GT Coupe 2006': 114, 'Ford Mustang Convertible 2007': 115, 'Ford Ranger SuperCab 2011': 116, 'GMC Acadia SUV 2012': 117, 'GMC Canyon Extended Cab 2012': 118, 'GMC Savana Van 2012': 119, 'GMC Terrain SUV 2012': 120, 'GMC Yukon Hybrid SUV 2012': 121, 'Geo Metro Convertible 1993': 122, 'HUMMER H2 SUT Crew Cab 2009': 123, 'HUMMER H3T Crew Cab 2010': 124, 'Honda Accord Coupe 2012': 125, 'Honda Accord Sedan 2012': 126, 'Honda Odyssey Minivan 2007': 127, 'Honda Odyssey Minivan 2012': 128, 'Hyundai Accent Sedan 2012': 129, 'Hyundai Azera Sedan 2012': 130, 'Hyundai Elantra Sedan 2007': 131, 'Hyundai Elantra Touring Hatchback 2012': 132, 'Hyundai Genesis Sedan 2012': 133, 'Hyundai Santa Fe SUV 2012': 134, 'Hyundai Sonata Hybrid Sedan 2012': 135, 'Hyundai Sonata Sedan 2012': 136, 'Hyundai Tucson SUV 2012': 137, 'Hyundai Veloster Hatchback 2012': 138, 'Hyundai Veracruz SUV 2012': 139, 'Infiniti G Coupe IPL 2012': 140, 'Infiniti QX56 SUV 2011': 141, 'Isuzu Ascender SUV 2008': 142, 'Jaguar XK XKR 2012': 143, 'Jeep Compass SUV 2012': 144, 'Jeep Grand Cherokee SUV 2012': 145, 'Jeep Liberty SUV 2012': 146, 'Jeep Patriot SUV 2012': 147, 'Jeep Wrangler SUV 2012': 148, 'Lamborghini Aventador Coupe 2012': 149, 'Lamborghini Diablo Coupe 2001': 150, 'Lamborghini Gallardo LP 570-4 Superleggera 2012': 151, 'Lamborghini Reventon Coupe 2008': 152, 'Land Rover LR2 SUV 2012': 153, 'Land Rover Range Rover SUV 2012': 154, 'Lincoln Town Car Sedan 2011': 155, 'MINI Cooper Roadster Convertible 2012': 156, 'Maybach Landaulet Convertible 2012': 157, 'Mazda Tribute SUV 2011': 158, 'McLaren MP4-12C Coupe 2012': 159, 'Mercedes-Benz 300-Class Convertible 1993': 160, 'Mercedes-Benz C-Class Sedan 2012': 161, 'Mercedes-Benz E-Class Sedan 2012': 162, 'Mercedes-Benz S-Class Sedan 2012': 163, 'Mercedes-Benz SL-Class Coupe 2009': 164, 'Mercedes-Benz Sprinter Van 2012': 165, 'Mitsubishi Lancer Sedan 2012': 166, 'Nissan 240SX Coupe 1998': 167, 'Nissan Juke Hatchback 2012': 168, 'Nissan Leaf Hatchback 2012': 169, 'Nissan NV Passenger Van 2012': 170, 'Plymouth Neon Coupe 1999': 171, 'Porsche Panamera Sedan 2012': 172, 'Ram C-V Cargo Van Minivan 2012': 173, 'Rolls-Royce Ghost Sedan 2012': 174, 'Rolls-Royce Phantom Drophead Coupe Convertible 2012': 175, 'Rolls-Royce Phantom Sedan 2012': 176, 'Scion xD Hatchback 2012': 177, 'Spyker C8 Convertible 2009': 178, 'Spyker C8 Coupe 2009': 179, 'Suzuki Aerio Sedan 2007': 180, 'Suzuki Kizashi Sedan 2012': 181, 'Suzuki SX4 Hatchback 2012': 182, 'Suzuki SX4 Sedan 2012': 183, 'Tesla Model S Sedan 2012': 184, 'Toyota 4Runner SUV 2012': 185, 'Toyota Camry Sedan 2012': 186, 'Toyota Corolla Sedan 2012': 187, 'Toyota Sequoia SUV 2012': 188, 'Volkswagen Beetle Hatchback 2012': 189, 'Volkswagen Golf Hatchback 1991': 190, 'Volkswagen Golf Hatchback 2012': 191, 'Volvo 240 Sedan 1993': 192, 'Volvo C30 Hatchback 2012': 193, 'Volvo XC90 SUV 2007': 194, 'smart fortwo Convertible 2012': 195}

# Create a reverse mapping
car_labels_list = [model for model, _ in sorted(car_labels_dict.items(), key=lambda item: item[1])]

# Define a function to load the model
def load_model(model_path, num_classes):
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path))
    return model

# Load the model
model_save_path = "model.pth"
model = load_model(model_save_path, num_classes)
model.eval()

# Define the transformation (must be the same as used during training)
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def classify_image(image_path):
    # Load the image
    image = Image.open(image_path)
    
    # Define the image transformation pipeline
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Apply the transformation to the image
    image = transform(image).unsqueeze(0)
    
    # Load the pre-trained model
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load('model.pth', map_location=torch.device('cpu')))
    model.eval()
    
    # Perform the prediction
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_class = torch.max(probabilities, 1)
    
    # Return the class index and confidence score
    return predicted_class.item(), confidence.item()


# Define a function to get the label from the predicted class index
def get_label(class_index):
    try:
        return car_labels_list[class_index]
    except IndexError:
        return "Unknown"