from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import json

tourism_bp = Blueprint('tourism', __name__)

# Mock data for archaeological sites
archaeological_sites = [
    {
        'id': 1,
        'name': {'ar': 'الأهرامات الكبرى', 'en': 'Great Pyramids of Giza'},
        'location': {'ar': 'الجيزة، مصر', 'en': 'Giza, Egypt'},
        'period': {'ar': '2580-2510 ق.م', 'en': '2580-2510 BC'},
        'discovered': {'ar': 'معروفة منذ القدم', 'en': 'Known since ancient times'},
        'description': {
            'ar': 'واحدة من عجائب الدنيا السبع القديمة، تضم ثلاثة أهرامات رئيسية بناها الفراعنة خوفو وخفرع ومنكاورع',
            'en': 'One of the Seven Wonders of the Ancient World, featuring three main pyramids built by pharaohs Khufu, Khafre, and Menkaure'
        },
        'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d73d0e?w=400&h=300&fit=crop',
        'coordinates': {'lat': 29.9792, 'lng': 31.1342},
        'entry_fee': {'adult': 200, 'child': 100, 'currency': 'EGP'},
        'opening_hours': {'open': '08:00', 'close': '17:00'},
        'best_visit_time': {'ar': 'أكتوبر - أبريل', 'en': 'October - April'}
    },
    {
        'id': 2,
        'name': {'ar': 'ماchu Picchu', 'en': 'Machu Picchu'},
        'location': {'ar': 'كوسكو، بيرو', 'en': 'Cusco, Peru'},
        'period': {'ar': '1450 م', 'en': '1450 AD'},
        'discovered': {'ar': '1911 م', 'en': '1911 AD'},
        'description': {
            'ar': 'مدينة الإنكا المفقودة في جبال الأنديز، تقع على ارتفاع 2430 متر فوق سطح البحر',
            'en': 'The Lost City of the Incas in the Andes Mountains, located 2,430 meters above sea level'
        },
        'image': 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=400&h=300&fit=crop',
        'coordinates': {'lat': -13.1631, 'lng': -72.5450},
        'entry_fee': {'adult': 152, 'child': 70, 'currency': 'USD'},
        'opening_hours': {'open': '06:00', 'close': '17:30'},
        'best_visit_time': {'ar': 'مايو - سبتمبر', 'en': 'May - September'}
    },
    {
        'id': 3,
        'name': {'ar': 'البتراء', 'en': 'Petra'},
        'location': {'ar': 'الأردن', 'en': 'Jordan'},
        'period': {'ar': '312 ق.م', 'en': '312 BC'},
        'discovered': {'ar': '1812 م', 'en': '1812 AD'},
        'description': {
            'ar': 'المدينة الوردية المنحوتة في الصخر، عاصمة مملكة الأنباط القديمة',
            'en': 'The Rose City carved into rock, ancient capital of the Nabataean Kingdom'
        },
        'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop',
        'coordinates': {'lat': 30.3285, 'lng': 35.4444},
        'entry_fee': {'adult': 50, 'child': 25, 'currency': 'JOD'},
        'opening_hours': {'open': '06:00', 'close': '18:00'},
        'best_visit_time': {'ar': 'مارس - مايو، سبتمبر - نوفمبر', 'en': 'March - May, September - November'}
    },
    {
        'id': 4,
        'name': {'ar': 'الكولوسيوم', 'en': 'Colosseum'},
        'location': {'ar': 'روما، إيطاليا', 'en': 'Rome, Italy'},
        'period': {'ar': '72-80 م', 'en': '72-80 AD'},
        'discovered': {'ar': 'معروف منذ القدم', 'en': 'Known since ancient times'},
        'description': {
            'ar': 'أكبر مدرج روماني في العالم، يتسع لـ 50,000 متفرج',
            'en': 'The largest Roman amphitheater in the world, with a capacity of 50,000 spectators'
        },
        'image': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&h=300&fit=crop',
        'coordinates': {'lat': 41.8902, 'lng': 12.4922},
        'entry_fee': {'adult': 16, 'child': 0, 'currency': 'EUR'},
        'opening_hours': {'open': '08:30', 'close': '19:15'},
        'best_visit_time': {'ar': 'أبريل - يونيو، سبتمبر - أكتوبر', 'en': 'April - June, September - October'}
    }
]

# Mock data for luxury hotels
luxury_hotels = [
    {
        'id': 1,
        'name': {'ar': 'فندق برج العرب', 'en': 'Burj Al Arab'},
        'location': {'ar': 'دبي، الإمارات', 'en': 'Dubai, UAE'},
        'rating': 5,
        'price': {'amount': 2500, 'currency': 'AED'},
        'description': {
            'ar': 'فندق فاخر على شكل شراع يقع على جزيرة اصطناعية',
            'en': 'Luxury sail-shaped hotel located on an artificial island'
        },
        'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=300&fit=crop',
        'coordinates': {'lat': 25.1413, 'lng': 55.1853},
        'amenities': {
            'ar': ['سبا', 'مسبح', 'مطاعم فاخرة', 'خدمة الغرف 24/7', 'واي فاي مجاني'],
            'en': ['Spa', 'Swimming Pool', 'Fine Dining', '24/7 Room Service', 'Free WiFi']
        },
        'rooms': 202,
        'check_in': '15:00',
        'check_out': '12:00'
    },
    {
        'id': 2,
        'name': {'ar': 'فندق ريتز كارلتون', 'en': 'The Ritz-Carlton'},
        'location': {'ar': 'باريس، فرنسا', 'en': 'Paris, France'},
        'rating': 5,
        'price': {'amount': 800, 'currency': 'EUR'},
        'description': {
            'ar': 'فندق فاخر في قلب باريس بإطلالة على ساحة فاندوم',
            'en': 'Luxury hotel in the heart of Paris overlooking Place Vendôme'
        },
        'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400&h=300&fit=crop',
        'coordinates': {'lat': 48.8676, 'lng': 2.3292},
        'amenities': {
            'ar': ['سبا', 'صالة رياضية', 'مطاعم حائزة على نجوم ميشلان', 'خدمة كونسيرج'],
            'en': ['Spa', 'Fitness Center', 'Michelin-starred restaurants', 'Concierge Service']
        },
        'rooms': 142,
        'check_in': '15:00',
        'check_out': '12:00'
    },
    {
        'id': 3,
        'name': {'ar': 'فندق أمان طوكيو', 'en': 'Aman Tokyo'},
        'location': {'ar': 'طوكيو، اليابان', 'en': 'Tokyo, Japan'},
        'rating': 5,
        'price': {'amount': 1200, 'currency': 'USD'},
        'description': {
            'ar': 'فندق فاخر بتصميم ياباني معاصر في قلب طوكيو',
            'en': 'Luxury hotel with contemporary Japanese design in the heart of Tokyo'
        },
        'image': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&h=300&fit=crop',
        'coordinates': {'lat': 35.6762, 'lng': 139.6503},
        'amenities': {
            'ar': ['سبا ياباني تقليدي', 'مسبح', 'حديقة يابانية', 'مطاعم يابانية أصيلة'],
            'en': ['Traditional Japanese Spa', 'Swimming Pool', 'Japanese Garden', 'Authentic Japanese Restaurants']
        },
        'rooms': 84,
        'check_in': '15:00',
        'check_out': '12:00'
    }
]

# Mock data for user trips
user_trips = [
    {
        'id': 1,
        'name': {'ar': 'رحلة مصر الأثرية', 'en': 'Egypt Archaeological Tour'},
        'destination': {'ar': 'القاهرة والأقصر', 'en': 'Cairo & Luxor'},
        'start_date': '2024-03-15',
        'end_date': '2024-03-22',
        'duration': 7,
        'status': {'ar': 'قيد التخطيط', 'en': 'Planning'},
        'travelers': 2,
        'sites': [1],  # Pyramids
        'hotels': [],
        'budget': {'amount': 3000, 'currency': 'USD'}
    },
    {
        'id': 2,
        'name': {'ar': 'رحلة أوروبا الفاخرة', 'en': 'Luxury Europe Trip'},
        'destination': {'ar': 'باريس وروما', 'en': 'Paris & Rome'},
        'start_date': '2024-05-10',
        'end_date': '2024-05-20',
        'duration': 10,
        'status': {'ar': 'مؤكدة', 'en': 'Confirmed'},
        'travelers': 2,
        'sites': [4],  # Colosseum
        'hotels': [2],  # Ritz-Carlton Paris
        'budget': {'amount': 8000, 'currency': 'EUR'}
    }
]

@tourism_bp.route('/sites', methods=['GET'])
def get_archaeological_sites():
    """Get all archaeological sites"""
    language = request.args.get('lang', 'en')
    search = request.args.get('search', '').lower()
    
    filtered_sites = archaeological_sites
    if search:
        filtered_sites = [
            site for site in archaeological_sites 
            if search in site['name'][language].lower() or 
               search in site['location'][language].lower()
        ]
    
    return jsonify({
        'success': True,
        'data': filtered_sites,
        'count': len(filtered_sites)
    })

@tourism_bp.route('/sites/<int:site_id>', methods=['GET'])
def get_site_details(site_id):
    """Get detailed information about a specific archaeological site"""
    site = next((s for s in archaeological_sites if s['id'] == site_id), None)
    if not site:
        return jsonify({'success': False, 'message': 'Site not found'}), 404
    
    return jsonify({
        'success': True,
        'data': site
    })

@tourism_bp.route('/hotels', methods=['GET'])
def get_luxury_hotels():
    """Get all luxury hotels"""
    language = request.args.get('lang', 'en')
    search = request.args.get('search', '').lower()
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    
    filtered_hotels = luxury_hotels
    if search:
        filtered_hotels = [
            hotel for hotel in filtered_hotels 
            if search in hotel['name'][language].lower() or 
               search in hotel['location'][language].lower()
        ]
    
    if min_price is not None:
        filtered_hotels = [h for h in filtered_hotels if h['price']['amount'] >= min_price]
    
    if max_price is not None:
        filtered_hotels = [h for h in filtered_hotels if h['price']['amount'] <= max_price]
    
    return jsonify({
        'success': True,
        'data': filtered_hotels,
        'count': len(filtered_hotels)
    })

@tourism_bp.route('/hotels/<int:hotel_id>', methods=['GET'])
def get_hotel_details(hotel_id):
    """Get detailed information about a specific hotel"""
    hotel = next((h for h in luxury_hotels if h['id'] == hotel_id), None)
    if not hotel:
        return jsonify({'success': False, 'message': 'Hotel not found'}), 404
    
    return jsonify({
        'success': True,
        'data': hotel
    })

@tourism_bp.route('/hotels/<int:hotel_id>/book', methods=['POST'])
def book_hotel(hotel_id):
    """Book a hotel room"""
    hotel = next((h for h in luxury_hotels if h['id'] == hotel_id), None)
    if not hotel:
        return jsonify({'success': False, 'message': 'Hotel not found'}), 404
    
    data = request.get_json()
    required_fields = ['check_in', 'check_out', 'guests', 'name', 'email']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Calculate total price (mock calculation)
    check_in = datetime.strptime(data['check_in'], '%Y-%m-%d')
    check_out = datetime.strptime(data['check_out'], '%Y-%m-%d')
    nights = (check_out - check_in).days
    total_price = nights * hotel['price']['amount']
    
    booking = {
        'id': f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'hotel_id': hotel_id,
        'hotel_name': hotel['name'],
        'check_in': data['check_in'],
        'check_out': data['check_out'],
        'nights': nights,
        'guests': data['guests'],
        'total_price': total_price,
        'currency': hotel['price']['currency'],
        'guest_info': {
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone', '')
        },
        'status': 'confirmed',
        'booking_date': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'message': 'Hotel booked successfully',
        'data': booking
    })

@tourism_bp.route('/trips', methods=['GET'])
def get_user_trips():
    """Get all user trips"""
    return jsonify({
        'success': True,
        'data': user_trips,
        'count': len(user_trips)
    })

@tourism_bp.route('/trips', methods=['POST'])
def create_trip():
    """Create a new trip"""
    data = request.get_json()
    required_fields = ['name', 'destination', 'start_date', 'end_date', 'travelers']
    
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
    
    # Calculate duration
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    duration = (end_date - start_date).days
    
    new_trip = {
        'id': len(user_trips) + 1,
        'name': {'ar': data['name'], 'en': data['name']},
        'destination': {'ar': data['destination'], 'en': data['destination']},
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'duration': duration,
        'status': {'ar': 'قيد التخطيط', 'en': 'Planning'},
        'travelers': data['travelers'],
        'sites': [],
        'hotels': [],
        'budget': data.get('budget', {'amount': 0, 'currency': 'USD'})
    }
    
    user_trips.append(new_trip)
    
    return jsonify({
        'success': True,
        'message': 'Trip created successfully',
        'data': new_trip
    }), 201

@tourism_bp.route('/trips/<int:trip_id>', methods=['GET'])
def get_trip_details(trip_id):
    """Get detailed information about a specific trip"""
    trip = next((t for t in user_trips if t['id'] == trip_id), None)
    if not trip:
        return jsonify({'success': False, 'message': 'Trip not found'}), 404
    
    # Add detailed site and hotel information
    trip_details = trip.copy()
    trip_details['site_details'] = [
        next((s for s in archaeological_sites if s['id'] == site_id), None)
        for site_id in trip['sites']
    ]
    trip_details['hotel_details'] = [
        next((h for h in luxury_hotels if h['id'] == hotel_id), None)
        for hotel_id in trip['hotels']
    ]
    
    return jsonify({
        'success': True,
        'data': trip_details
    })

@tourism_bp.route('/trips/<int:trip_id>/add-site', methods=['POST'])
def add_site_to_trip(trip_id):
    """Add an archaeological site to a trip"""
    trip = next((t for t in user_trips if t['id'] == trip_id), None)
    if not trip:
        return jsonify({'success': False, 'message': 'Trip not found'}), 404
    
    data = request.get_json()
    site_id = data.get('site_id')
    
    if not site_id:
        return jsonify({'success': False, 'message': 'Missing site_id'}), 400
    
    site = next((s for s in archaeological_sites if s['id'] == site_id), None)
    if not site:
        return jsonify({'success': False, 'message': 'Site not found'}), 404
    
    if site_id not in trip['sites']:
        trip['sites'].append(site_id)
    
    return jsonify({
        'success': True,
        'message': 'Site added to trip successfully',
        'data': trip
    })

@tourism_bp.route('/trips/<int:trip_id>/add-hotel', methods=['POST'])
def add_hotel_to_trip(trip_id):
    """Add a hotel to a trip"""
    trip = next((t for t in user_trips if t['id'] == trip_id), None)
    if not trip:
        return jsonify({'success': False, 'message': 'Trip not found'}), 404
    
    data = request.get_json()
    hotel_id = data.get('hotel_id')
    
    if not hotel_id:
        return jsonify({'success': False, 'message': 'Missing hotel_id'}), 400
    
    hotel = next((h for h in luxury_hotels if h['id'] == hotel_id), None)
    if not hotel:
        return jsonify({'success': False, 'message': 'Hotel not found'}), 404
    
    if hotel_id not in trip['hotels']:
        trip['hotels'].append(hotel_id)
    
    return jsonify({
        'success': True,
        'message': 'Hotel added to trip successfully',
        'data': trip
    })

@tourism_bp.route('/search', methods=['GET'])
def search_all():
    """Search across all sites and hotels"""
    query = request.args.get('q', '').lower()
    language = request.args.get('lang', 'en')
    
    if not query:
        return jsonify({'success': False, 'message': 'Search query is required'}), 400
    
    # Search sites
    matching_sites = [
        site for site in archaeological_sites 
        if query in site['name'][language].lower() or 
           query in site['location'][language].lower() or
           query in site['description'][language].lower()
    ]
    
    # Search hotels
    matching_hotels = [
        hotel for hotel in luxury_hotels 
        if query in hotel['name'][language].lower() or 
           query in hotel['location'][language].lower() or
           query in hotel['description'][language].lower()
    ]
    
    return jsonify({
        'success': True,
        'data': {
            'sites': matching_sites,
            'hotels': matching_hotels
        },
        'count': {
            'sites': len(matching_sites),
            'hotels': len(matching_hotels),
            'total': len(matching_sites) + len(matching_hotels)
        }
    })

