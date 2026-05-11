export default function Importante(){
    return(
      <div className="m-3">
        <h2 className="fw-bold mb-1">Error 2̛̛̰̙̠̯̞̟͙̜̯̉͆̈́̍͊̌̃͜͟͞͡2̛̱͇͕̰̫̝͙͋̎̅͋̀̔̕̚͢͜͠͝ͅͅ2̛͉̞͉̗͔̖̬̱̱͖̯̊͂͊͌͂̓̆͘̚͘:̧͓͚͎͉͔̲̠̠͉̍̉̉̓̈̉̍̏̓͢͝͞ Como llegaste aquí</h2>
        <p className="mb-4 c-muted">Esto no se supone que lo viera alguien más, lol.</p>
        <div className="row g-3">
          {[
            { gif: "https://i.pinimg.com/originals/29/09/ba/2909ba9ad145bdb5beaace18ec796c23.gif",alt:"Gato Bailando"},
            { gif: "https://media.tenor.com/Us7zpL-oxHoAAAAM/gato-baile-jajalol.gif",alt:"Gato Bailando"},
            { gif: "https://i.pinimg.com/originals/ab/43/ac/ab43ac3b607ebdfd2995c0a2c0b1a63d.gif",alt:"Gato Bailando"},
            { gif: "https://media.tenor.com/0Q5IZ6e9pC8AAAAM/cat-cute-cat.gif",alt:"Gato Bailando"}
            ].map((gif, i) => (
            <div key={i} className="col-auto col-sm-auto col-lg-auto align-content-center d-flex justify-content-center">
              <div className="p-2 rounded-4 h-100 importante-card">
                <img src={gif.gif} alt={gif.alt} className="fs-1 mb-1 image-fluid rounded-4 importante-icon" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
}