import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [language, setLanguage] = useState('ar');
  const [activeTab, setActiveTab] = useState('sites');
  const [searchQuery, setSearchQuery] = useState('');
  const [sites, setSites] = useState([]);
  const [hotels, setHotels] = useState([]);
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_BASE = '/api/tourism';

  const toggleLanguage = () => {
    setLanguage(language === 'ar' ? 'en' : 'ar');
  };

  const content = {
    ar: {
      title: 'منصة السياحة العالمية',
      subtitle: 'اكتشف أجمل المواقع الأثرية والفنادق الفاخرة حول العالم',
      searchPlaceholder: 'ابحث عن وجهتك المثالية...',
      searchButton: 'بحث',
      tabs: {
        sites: 'المواقع الأثرية',
        hotels: 'الفنادق الفاخرة',
        planner: 'مخطط الرحلات'
      },
      viewDetails: 'عرض التفاصيل',
      bookNow: 'احجز الآن',
      myTrips: 'رحلاتي',
      createTrip: 'إنشاء رحلة جديدة',
      tripName: 'اسم الرحلة',
      destination: 'الوجهة',
      startDate: 'تاريخ البداية',
      endDate: 'تاريخ النهاية',
      travelers: 'عدد المسافرين',
      createButton: 'إنشاء الرحلة',
      loading: 'جاري التحميل...',
      discovered: 'تاريخ الاكتشاف',
      entryFee: 'رسوم الدخول',
      openingHours: 'ساعات العمل',
      bestTime: 'أفضل وقت للزيارة',
      rating: 'التقييم',
      amenities: 'المرافق',
      rooms: 'عدد الغرف'
    },
    en: {
      title: 'Global Tourism Platform',
      subtitle: 'Discover the most beautiful archaeological sites and luxury hotels around the world',
      searchPlaceholder: 'Search for your perfect destination...',
      searchButton: 'Search',
      tabs: {
        sites: 'Archaeological Sites',
        hotels: 'Luxury Hotels',
        planner: 'Travel Planner'
      },
      viewDetails: 'View Details',
      bookNow: 'Book Now',
      myTrips: 'My Trips',
      createTrip: 'Create New Trip',
      tripName: 'Trip Name',
      destination: 'Destination',
      startDate: 'Start Date',
      endDate: 'End Date',
      travelers: 'Number of Travelers',
      createButton: 'Create Trip',
      loading: 'Loading...',
      discovered: 'Discovered',
      entryFee: 'Entry Fee',
      openingHours: 'Opening Hours',
      bestTime: 'Best Time to Visit',
      rating: 'Rating',
      amenities: 'Amenities',
      rooms: 'Rooms'
    }
  };

  // Fetch archaeological sites
  const fetchSites = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/sites?lang=${language}&search=${searchQuery}`);
      const data = await response.json();
      if (data.success) {
        setSites(data.data);
      }
    } catch (error) {
      console.error('Error fetching sites:', error);
    }
    setLoading(false);
  };

  // Fetch luxury hotels
  const fetchHotels = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/hotels?lang=${language}&search=${searchQuery}`);
      const data = await response.json();
      if (data.success) {
        setHotels(data.data);
      }
    } catch (error) {
      console.error('Error fetching hotels:', error);
    }
    setLoading(false);
  };

  // Fetch user trips
  const fetchTrips = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/trips`);
      const data = await response.json();
      if (data.success) {
        setTrips(data.data);
      }
    } catch (error) {
      console.error('Error fetching trips:', error);
    }
    setLoading(false);
  };

  // Create new trip
  const createTrip = async (tripData) => {
    try {
      const response = await fetch(`${API_BASE}/trips`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tripData),
      });
      const data = await response.json();
      if (data.success) {
        fetchTrips(); // Refresh trips list
        return true;
      }
    } catch (error) {
      console.error('Error creating trip:', error);
    }
    return false;
  };

  // Load data when component mounts or language changes
  useEffect(() => {
    fetchSites();
    fetchHotels();
    fetchTrips();
  }, [language]);

  // Search functionality
  useEffect(() => {
    if (activeTab === 'sites') {
      fetchSites();
    } else if (activeTab === 'hotels') {
      fetchHotels();
    }
  }, [searchQuery]);

  const renderSites = () => (
    <div className="grid">
      {loading ? (
        <div className="loading">{content[language].loading}</div>
      ) : (
        sites.map(site => (
          <div key={site.id} className="card">
            <img src={site.image} alt={site.name[language]} />
            <div className="card-content">
              <h3>{site.name[language]}</h3>
              <p className="location">📍 {site.location[language]}</p>
              <p className="period">🏛️ {site.period[language]}</p>
              <p className="discovered">🔍 {content[language].discovered}: {site.discovered[language]}</p>
              <p className="description">{site.description[language]}</p>
              <div className="site-details">
                <p className="entry-fee">💰 {content[language].entryFee}: {site.entry_fee.adult} {site.entry_fee.currency}</p>
                <p className="hours">🕒 {content[language].openingHours}: {site.opening_hours.open} - {site.opening_hours.close}</p>
                <p className="best-time">🌟 {content[language].bestTime}: {site.best_visit_time[language]}</p>
              </div>
              <button className="btn-primary">{content[language].viewDetails}</button>
            </div>
          </div>
        ))
      )}
    </div>
  );

  const renderHotels = () => (
    <div className="grid">
      {loading ? (
        <div className="loading">{content[language].loading}</div>
      ) : (
        hotels.map(hotel => (
          <div key={hotel.id} className="card">
            <img src={hotel.image} alt={hotel.name[language]} />
            <div className="card-content">
              <h3>{hotel.name[language]}</h3>
              <p className="location">📍 {hotel.location[language]}</p>
              <div className="rating">
                ⭐ {'★'.repeat(hotel.rating)} ({hotel.rating}/5)
              </div>
              <p className="price">💰 {hotel.price.amount} {hotel.price.currency} {language === 'ar' ? 'لليلة' : 'per night'}</p>
              <p className="description">{hotel.description[language]}</p>
              <div className="hotel-details">
                <p className="rooms">🏨 {content[language].rooms}: {hotel.rooms}</p>
                <p className="checkin">🕐 Check-in: {hotel.check_in} | Check-out: {hotel.check_out}</p>
                <div className="amenities">
                  <p>🎯 {content[language].amenities}:</p>
                  <ul>
                    {hotel.amenities[language].slice(0, 3).map((amenity, index) => (
                      <li key={index}>{amenity}</li>
                    ))}
                  </ul>
                </div>
              </div>
              <button className="btn-primary">{content[language].bookNow}</button>
            </div>
          </div>
        ))
      )}
    </div>
  );

  const renderPlanner = () => {
    const [tripForm, setTripForm] = useState({
      name: '',
      destination: '',
      start_date: '',
      end_date: '',
      travelers: 1
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      const success = await createTrip(tripForm);
      if (success) {
        setTripForm({
          name: '',
          destination: '',
          start_date: '',
          end_date: '',
          travelers: 1
        });
      }
    };

    return (
      <div className="planner-container">
        <div className="planner-section">
          <h3>{content[language].myTrips}</h3>
          <div className="trips-list">
            {loading ? (
              <div className="loading">{content[language].loading}</div>
            ) : (
              trips.map(trip => (
                <div key={trip.id} className="trip-card">
                  <h4>{trip.name[language]}</h4>
                  <p>📍 {trip.destination[language]}</p>
                  <p>📅 {trip.duration} {language === 'ar' ? 'أيام' : 'days'}</p>
                  <p>📊 {trip.status[language]}</p>
                  <p>👥 {trip.travelers} {language === 'ar' ? 'مسافر' : 'travelers'}</p>
                  <button className="btn-secondary">{content[language].viewDetails}</button>
                </div>
              ))
            )}
          </div>
        </div>
        
        <div className="planner-section">
          <h3>{content[language].createTrip}</h3>
          <form className="trip-form" onSubmit={handleSubmit}>
            <input 
              type="text" 
              placeholder={content[language].tripName}
              value={tripForm.name}
              onChange={(e) => setTripForm({...tripForm, name: e.target.value})}
              required
            />
            <input 
              type="text" 
              placeholder={content[language].destination}
              value={tripForm.destination}
              onChange={(e) => setTripForm({...tripForm, destination: e.target.value})}
              required
            />
            <input 
              type="date"
              value={tripForm.start_date}
              onChange={(e) => setTripForm({...tripForm, start_date: e.target.value})}
              required
            />
            <input 
              type="date"
              value={tripForm.end_date}
              onChange={(e) => setTripForm({...tripForm, end_date: e.target.value})}
              required
            />
            <input 
              type="number" 
              placeholder={content[language].travelers}
              min="1"
              value={tripForm.travelers}
              onChange={(e) => setTripForm({...tripForm, travelers: parseInt(e.target.value)})}
              required
            />
            <button type="submit" className="btn-primary">{content[language].createButton}</button>
          </form>
        </div>
      </div>
    );
  };

  return (
    <div className={`App ${language}`}>
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <h1>🌍 {content[language].title}</h1>
            </div>
            <button className="language-toggle" onClick={toggleLanguage}>
              {language === 'ar' ? 'English' : 'العربية'}
            </button>
          </div>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <div className="container">
            <h2 className="hero-title">{content[language].subtitle}</h2>
            <div className="search-bar">
              <input 
                type="text" 
                placeholder={content[language].searchPlaceholder}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button className="search-btn">{content[language].searchButton}</button>
            </div>
          </div>
        </section>

        <section className="content">
          <div className="container">
            <div className="tabs">
              <button 
                className={`tab ${activeTab === 'sites' ? 'active' : ''}`}
                onClick={() => setActiveTab('sites')}
              >
                🏛️ {content[language].tabs.sites}
              </button>
              <button 
                className={`tab ${activeTab === 'hotels' ? 'active' : ''}`}
                onClick={() => setActiveTab('hotels')}
              >
                🏨 {content[language].tabs.hotels}
              </button>
              <button 
                className={`tab ${activeTab === 'planner' ? 'active' : ''}`}
                onClick={() => setActiveTab('planner')}
              >
                📅 {content[language].tabs.planner}
              </button>
            </div>

            <div className="tab-content">
              {activeTab === 'sites' && renderSites()}
              {activeTab === 'hotels' && renderHotels()}
              {activeTab === 'planner' && renderPlanner()}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;

