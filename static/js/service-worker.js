
var CACHE_NAME = 'mapartotheque-v1';


self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
  );
});


self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((resp) => {
            if (isValid(resp)) {
                return resp;
            }
            return fetch(event.request).then((response) => {
                let responseClone = response.clone();
                event.waitUntil(caches.open('api').then(function (cache) {
                    var headers = new Headers(responseClone.headers);
                    headers.append("sw-fetched-on", new Date().getTime());

                    return responseClone.blob().then(function (body) {
                        cache.put(event.request, new Response(body, {
                            status: responseClone.status,
                            statusText: responseClone.statusText,
                            headers: headers
                        }));
                    });
                }));
                return response
            }).catch(() => {
                return caches.match(request).then(function (response) {
                    return caches.match('./sw-test/gallery/myLittleVader.jpg');
                });
            });
        }));
});

/**
 * Check if cached API data is still valid
 * @param  {Object}  response The response object
 * @return {Boolean}          If true, cached data is valid
 */
var isValid = function (response) {
    if (!response) return false;
    var fetched = response.headers.get('sw-fetched-on');
    if (fetched && (parseFloat(fetched) + (1000 * 60 * 60 * 24)) > new Date().getTime()) return true;
    return false;
};