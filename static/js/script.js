function onTitleChange() {
	var champIdentifiant = document.getElementById("identifiant");

	var titre = document.getElementById("titre");
	if (titre === "") {
		champIdentifiant.value = "";
		champIdentifiant.disabled = true;
	} else {
		champIdentifiant.disabled = false;

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function () {
		if (xhr.readyState === XMLHttpRequest.DONE) {
			if (xhr.status === 200) {
				champIdentifiant.innerHTML = xhr.responseText;
				champIdentifiant.value = xhr.responseText;
			} else {
				console.log('Erreur de serveur');
			}
		}
	};
	var titre = titre.value;
	titre = titre.replace(/\s+/g, '-').toLowerCase();
	xhr.open("GET", "/batir-ident/"+titre, true);
	console.log("vient de faire son open" + xhr.responseText)
	xhr.send();
	}

}