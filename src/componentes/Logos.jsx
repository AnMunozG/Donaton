export const DonatonLogo = ({ variante = "pequeño", width, height }) => {
  //Logo grande para el banner
  if (variante === "banner") {
    return (
      <svg
        width={width || "600"}
        height={height || "300"}
        viewBox="0 0 600 300"
        xmlns="http://www.w3.org/2000/svg"
      >
        <text
          x="150"
          y="160"
          className="logo-titulo-banner"
        >
          Donatón
        </text>

        {/* Corazón */}
        <path
          d="M120 150 
             C120 135, 140 130, 150 145 
             C160 130, 180 135, 180 150 
             C180 165, 150 185, 150 185 
             C150 185, 120 165, 120 150Z"
          fill="#dd4444"
        />

        {/* Subtítulo */}
        <text
          x="150"
          y="210"
          className="logo-subtitulo"
        >
          Coordinación de ayuda humanitaria
        </text>
      </svg>
    );
  }
  // Logo pequeño para header y footer
  return (
    <svg
      width={width || "300"}
      height={height || "100"}
      viewBox="0 0 300 100"
      xmlns="http://www.w3.org/2000/svg"
    >
      <text
        x="40"
        y="60"
        className="logo-titulo-small"
      >
        Donatón
      </text>

      {/* Corazón en la ó */}
      <path
        d="M185 30 
           C185 25, 190 22, 193 27 
           C196 22, 201 25, 201 30 
           C201 35, 193 40, 193 40 
           C193 40, 185 35, 185 30Z"
        fill="#dd4444"
      />
    </svg>
  );
};
