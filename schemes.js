// Full JSON data with rigorous eligibility criteria including income limits
const schemesData = [
  {
    "scheme_id": "AG001",
    "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "land_owned_hectares": {"max": 2},
      "age": {"min": 18},
      "citizenship": "Indian",
      "exclusions": ["former/taxpayer with income above threshold"]
    },
    "benefits": "₹6,000 per year in three equal installments via DBT",
    "link": "https://pmkisan.gov.in"
  },
  {
    "scheme_id": "AG002",
    "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "crop_type": ["food_crop", "oilseed", "horticulture"],
      "location": ["notified_districts"],
      "registration_before_sowing": true
    },
    "benefits": "Crop insurance: coverage for yield loss, prevented sowing, post-harvest losses",
    "link": "https://pmfby.gov.in"
  },
  {
    "scheme_id": "AG003",
    "name": "Pradhan Mantri Kisan Urja Suraksha evam Utthan Mahabhiyan (PM-KUSUM)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "land_owned_hectares": {"min": 1},
      "access_to_grid": true,
      "age": {"min": 18}
    },
    "benefits": "Subsidy for installing solar pumps; support for solar power use in irrigation",
    "link": "https://pmkusum.mnre.gov.in"
  },
  {
    "scheme_id": "AG004",
    "name": "Pradhan Mantri Kisan Maandhan Yojana (PM-KMY)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "land_owned_hectares": {"max": 2},
      "age": {"min": 18, "max": 40},
      "citizenship": "Indian",
      "exclusions": ["income_tax_payer", "government_employee", "already_member_of_NPS_ESIC_EPFO"]
    },
    "benefits": "Assured pension of ₹3,000 per month after the age of 60. Spouse eligible for 50% family pension after subscriber’s death.",
    "contribution": {
      "shared": "Equal monthly contribution by farmer and Government",
      "example": "Entry age 18 → ₹55/month; Entry age 40 → ₹200/month"
    },
    "implementation": {
      "mode": "Direct Benefit Transfer",
      "nodal_agency": "Ministry of Agriculture & Farmers Welfare, Government of India"
    },
    "link": "https://pmkmy.gov.in"
  },
  {
    "scheme_id": "AG005",
    "name": "Pradhan Mantri Krishi Sinchai Yojana (PMKSY)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "age": {"min": 18},
      "citizenship": "Indian",
      "land_owned_hectares": {"min": 0.1},
      "location": ["rural"],
      "priority_groups": ["small_farmers", "marginal_farmers", "watershed_areas", "drought_prone_areas"]
    },
    "benefits": "Financial assistance and subsidies for irrigation infrastructure, micro-irrigation (drip & sprinkler systems), watershed development, and improving on-farm water use efficiency.",
    "components": [
      "Accelerated Irrigation Benefit Programme (AIBP)",
      "Har Khet Ko Pani (HKKP)",
      "Per Drop More Crop (micro-irrigation)",
      "Watershed Development"
    ],
    "implementation": {
      "mode": "Central Sector & Centrally Sponsored Scheme components",
      "nodal_agency": "Ministry of Jal Shakti, Ministry of Agriculture & Farmers Welfare"
    },
    "link": "https://pmksy.gov.in"
  },
  {
    "scheme_id": "AG006",
    "name": "Soil Health Card Scheme",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "age": {"min": 18},
      "citizenship": "Indian",
      "land_owned_hectares": {"min": 0.1},
      "location": ["rural", "semi-urban"]
    },
    "benefits": "Free soil testing and issuance of Soil Health Cards every 3 years to farmers, providing recommendations on nutrient management and fertilizer use to improve soil health and crop productivity.",
    "link": "https://soilhealth.dac.gov.in"
  },
  {
    "scheme_id": "AG007",
    "name": "Kisan Credit Card (KCC)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer", "dairy_farmer", "fisherman", "poultry_farmer"],
      "age": {"min": 18, "max": 75},
      "citizenship": "Indian",
      "land_owned_hectares": {"min": 0.1},
      "joint_borrower_applicants": ["sharecroppers", "tenant_farmers", "oral_lessees"]
    },
    "benefits": "Provides short-term credit support for cultivation, post-harvest expenses, working capital for allied activities, and consumption needs. Interest subvention available for timely repayment.",
    "credit_limit": {
      "minimum": "Based on scale of finance and cropping pattern",
      "maximum": "Up to ₹3 lakh for crop loans; higher limits for allied activities"
    },
    "repayment_terms": {
      "crop_loan": "12 months or harvest season",
      "term_loan": "As per project requirements"
    },
    "implementation": {
      "mode": "Issued by banks (Public, Private, RRBs, Cooperative Banks)",
      "collateral": "Collateral-free up to ₹1.6 lakh",
      "insurance": "Covers crops under Pradhan Mantri Fasal Bima Yojana"
    },
    "link": "https://kcc.dac.gov.in"
  },
  {
    "scheme_id": "AG008",
    "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "age": {"min": 18},
      "citizenship": "Indian",
      "land_owned_hectares": {"min": 0.1},
      "group_based": true,
      "farmer_group_size": {"min": 20, "max": 50}
    },
    "benefits": "Financial assistance to promote cluster-based organic farming, certification support, organic input support, and market linkage for organic produce.",
    "objectives": [
      "Promote sustainable organic farming practices",
      "Reduce dependence on chemical fertilizers and pesticides",
      "Enhance soil fertility and biodiversity",
      "Support organic certification and branding"
    ],
    "implementation": {
      "mode": "Cluster-based approach (minimum 20 farmers, 50 acres)",
      "financial_assistance": "₹50,000 per hectare over 3 years (including organic inputs, certification, and training)",
      "nodal_agency": "Ministry of Agriculture & Farmers Welfare, Government of India"
    },
    "link": "https://pkvy.gov.in"
  },
  {
    "scheme_id": "AG009",
    "name": "National Food Security Mission (NFSM)",
    "category": "Farmer",
    "eligibility": {
      "occupation": ["farmer"],
      "age": {"min": 18},
      "citizenship": "Indian",
      "land_owned_hectares": {"min": 0.1},
      "priority_groups": ["small_farmers", "marginal_farmers", "SC", "ST", "women_farmers"]
    },
    "benefits": "Financial assistance, training, and input support to increase production of rice, wheat, pulses, coarse cereals, and commercial crops through productivity enhancement and technology promotion.",
    "objectives": [
      "Increase production and productivity of major food crops",
      "Promote sustainable agricultural practices",
      "Bridge yield gaps in identified districts",
      "Improve farm-level economy and food security"
    ],
    "implementation": {
      "mode": "Centrally Sponsored Scheme implemented through State Governments",
      "components": ["Rice Mission", "Wheat Mission", "Pulses Mission", "Coarse Cereals Mission", "Commercial Crops Mission (cotton, jute, sugarcane)"],
      "nodal_agency": "Department of Agriculture & Farmers Welfare, Government of India"
    },
    "link": "https://nfsm.gov.in"
  }
]


// Function to get URL parameters
function getURLParams() {
    const urlParams = new URLSearchParams(window.location.search);
    return {
        occupation: urlParams.get('occupation'),
        age: parseInt(urlParams.get('age')),
        income: parseInt(urlParams.get('income')),
        landOwned: parseFloat(urlParams.get('landOwned')),
        state: urlParams.get('state'),
        category: urlParams.getAll('category') // This gets all category values as an array
    };
}

// Function to check if user is eligible for a scheme
function isEligible(scheme, userData) {
    const eligibility = scheme.eligibility;
    
    if (eligibility.occupation && !eligibility.occupation.includes(userData.occupation)) {
        return false;
    }
    
    if (eligibility.age) {
        if (eligibility.age.min && userData.age < eligibility.age.min) return false;
        if (eligibility.age.max && userData.age > eligibility.age.max) return false;
    }
    
    if (eligibility.annual_income) {
        if (eligibility.annual_income.min && userData.income < eligibility.annual_income.min) return false;
        if (eligibility.annual_income.max && userData.income > eligibility.annual_income.max) return false;
    }
    
    if (eligibility.land_owned_hectares) {
        if (eligibility.land_owned_hectares.min && userData.landOwned < eligibility.land_owned_hectares.min) return false;
        if (eligibility.land_owned_hectares.max && userData.landOwned > eligibility.land_owned_hectares.max) return false;
    }
    
    if (eligibility.resident_state && eligibility.resident_state !== userData.state) {
        return false;
    }
    
    if (eligibility.exclusions) {
        if (eligibility.exclusions.includes("income_tax_payer") && userData.income > 500000) return false;
    }
    
    return true;
}

// Extract payment mode (with default)
function parsePaymentMode(scheme) {
    if (scheme.implementation && scheme.implementation.mode) {
        return scheme.implementation.mode;
    }
    
    const benefitsText = scheme.benefits || "";
    const modeMatch = benefitsText.match(/DBT|Direct Transfer|Bank Transfer|Cashless|Loan|Subsidy|Group funding|Stipend/i);
    return modeMatch ? modeMatch[0] : "Direct Benefit Transfer";
}

// Main function to render eligible schemes
function renderEligibleSchemes() {
    const userData = getURLParams();
    const schemesGrid = document.getElementById("schemesGrid");
    
    const eligibleSchemes = schemesData.filter(scheme => isEligible(scheme, userData));
    
    schemesGrid.innerHTML = "";
    
    if (eligibleSchemes.length === 0) {
        schemesGrid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 3rem;">
                <h2 style="color: #718096; margin-bottom: 1rem;">No Eligible Schemes Found</h2>
                <p style="color: #a0aec0;">Based on your provided information, no schemes match your eligibility criteria. Please check back later as new schemes may be added.</p>
                <a href="manualDataEntry.html" style="display: inline-block; margin-top: 2rem; padding: 1rem 2rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">Update Your Information</a>
            </div>
        `;
        return;
    }

    eligibleSchemes.forEach(scheme => {
        const paymentMode = parsePaymentMode(scheme);
        
        const contribution = scheme.contribution ? 
            `<div class="feature-item">
                <div class="feature-label">Contribution</div>
                <div class="feature-value">${scheme.contribution.shared}</div>
            </div>` : '';
            
        const components = scheme.components ? 
            `<div class="feature-item">
                <div class="feature-label">Components</div>
                <div class="feature-value">${scheme.components.slice(0, 2).join(', ')}${scheme.components.length > 2 ? '...' : ''}</div>
            </div>` : '';

        const card = document.createElement("div");
        card.classList.add("scheme-card");

        card.innerHTML = `
            <h3 class="scheme-title">${scheme.name}</h3>
            <div class="scheme-features">
                <div class="feature-item">
                    <div class="feature-label">Benefits</div>
                    <div class="feature-value">${scheme.benefits}</div>
                </div>
                <div class="feature-item">
                    <div class="feature-label">Payment Mode</div>
                    <div class="feature-value">${paymentMode}</div>
                </div>
                ${contribution}
                ${components}
            </div>
            <div class="scheme-actions">
                <a href="${scheme.link ? scheme.link : '#'}" class="action-btn btn-primary" target="_blank">Apply Now</a>
                <a href="#" class="action-btn btn-secondary" onclick="showSchemeDetails('${scheme.scheme_id}')">View Details</a>
            </div>
        `;

        schemesGrid.appendChild(card);
    });
    
    const headerSubtitle = document.querySelector('.header-subtitle');
    headerSubtitle.textContent = `Found ${eligibleSchemes.length} eligible scheme${eligibleSchemes.length !== 1 ? 's' : ''} for you`;
}

// Function to show scheme details
function showSchemeDetails(schemeId) {
    const scheme = schemesData.find(s => s.scheme_id === schemeId);
    if (scheme) {
        alert(`Details for ${scheme.name}:\n\n${scheme.benefits}\n\nFor more detailed information, please visit the official government portal: ${scheme.link || 'N/A'}`);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    renderEligibleSchemes();
});
