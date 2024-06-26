const apiUrl = 'http://localhost:5000/'

const toggleElement = document.getElementById('toggle-btn')
const selectNextElement = document.getElementById('select-next-btn')
const selectDiscoveredElement = document.getElementById('number-discovered')

//call discover when the page loads
discover()

// call discover every 90secs
setInterval(discover, 90*1000)

function discover(){
  fetchRequest(apiUrl + 'discover', 'PATCH').then((data) => {
    selectDiscoveredElement.innerHTML = data
  })
}

function fetchRequest(url, method) {
  const options = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
  }

  fetch(url, options)
    .then((response) => {
      console.log('Response object:', response)
      const contentType = response.headers.get('Content-Type')
      if (contentType && contentType.includes('application/json')) {
        return response.json() // Parse JSON response
      } else {
        return response.text() // Parse text response
      }
    })
    .then((data) => {
      console.log('Parsed response data:', data)
    })
    .catch((err) => {
      console.log('Fetch error:', err)
    })
}
