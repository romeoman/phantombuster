// Import required libraries
const axios = require('axios');

exports.main = async (event) => {
    // Extract the growth values from the event input
    const growth6Mth = event.inputFields.growth6Mth;
    const growth12Mth = event.inputFields.growth_12mth;
    const growth24Mth = event.inputFields.growth_24mth;

    const hsObjectId = event.object.objectId; // Assuming this ID is for a company

    // HubSpot configuration for the API call
    const hubspotConfig = {
        headers: {
            'Authorization': `Bearer ${process.env.ACCESSTOKEN}`,
            'Content-Type': 'application/json'
        }
    };

    // Data to update
    const companyData = {
        properties: {
            "growth_6mth": growth6Mth,
            "growth_12mth": growth12Mth,
            "growth_24mth": growth24Mth
        }
    };

    try {
        // Make a request to update the company in HubSpot
        const updateResponse = await axios.patch(`https://api.hubapi.com/crm/v3/objects/companies/${hsObjectId}`, companyData, hubspotConfig);

        if (updateResponse.status === 200) {
            console.log(`Company ${hsObjectId} updated successfully.`);
        } else {
            console.error(`Error updating company: ${updateResponse.statusText}`);
        }

    } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
            console.error(`HubSpot error: ${error.response.data.message}`);
        } else {
            console.error(`Error: ${error.message}`);
        }
    }
};
