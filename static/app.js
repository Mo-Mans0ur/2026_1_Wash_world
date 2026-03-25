
async function getName(){
    const conn = await fetch("api-get-name", {
        method : "POST"
    })

   const data = await conn.json()

   console.log(data)
   document.getElementById("the-name").innerHTML = data.name
}

