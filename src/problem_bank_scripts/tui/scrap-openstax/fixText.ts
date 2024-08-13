const textReplacements = {
    "–": "-",
    "“": '"',
    "”": '"',
    "’": "'",
    "‘": "'",
    "…": "...",
    "—": "-",
    "−": "-",
    "√": "$/sqrt$",
    "≈": "$\\approx$",
    "≠": "$\\neq$",
    "≤": "$\\leq$",
    "≥": "$\\geq$",
    "±": "$\\pm$",
    "×": "$\\times$",
    "÷": "$\\div$",
    " ": " ",
    "′": "'",
    "∣": "$\\mid$",
    ŷ: "$\\hat{y}$",
    β: "$\\beta$",
    α: "$\\alpha$",
    "°": "$^\\circ$",
    "∞": "$\\infty$",
    µ: "$\\mu$",
    "∑": "$\\sum$",
    "∏": "$\\prod$",
    "∂": "$\\partial$",
    "∆": "$\\Delta$",
    "∈": "$\\in$",
    "∉": "$\\notin$",
    "∅": "$\\emptyset$",
    "∩": "$\\cap$",
    "∪": "$\\cup$",
    '<em data-effect="italics">μ</em>': "$\\mu$",
    '<em data-effect="italics">σ</em>': "$\\sigma$",
    μ: "$\\mu$",
    σ: "$\\sigma$",
    "x¯x¯": "$\\bar{x}$",
    ΣX: "$\\Sigma X$",
    Σx: "$\\Sigma x$",
    ΣY: "$\\Sigma Y$",
    "\nα\n2\nα\n2\n": "$\\frac{\\alpha}{2}$",
    "s\nx\ns\nx\n": "$s_x$",
    "X\n¯\nX\n¯\n": "$\\bar{X}$",
    // '\n\nx\n¯\n\n\n\nx\n¯\n': '$\\bar{x}$',
    Χ: "X",
    // '\nX\n¯\nX\n¯\n': '$\\bar{X}$',
    // 'X\n  ¯\n \n\n\n  X\n  ¯\n': '$\\bar{X}$',
    "$^th$": "$^{th}$",
    '∼': '$\\sim$',
    'χ': 'X',
    '½': '$\\frac{1}{2}$',
    // '\nx\n¯\n\n\n\nx\n¯\n': '$\\bar{x}$',
    // '\nX\n  ¯\n \n\n\n  X\n  ¯\n': '$\\bar{X}$',
};

const endReplacements = {
    $$_: "_", // handle <sub>
    "$$^": "^", // handle <sup>
};

export const fixText = (text: string): string => {
    Object.entries(textReplacements)
        .sort((a, b) => b[0].length - a[0].length)
        .forEach(([key, value]) => {
            text = text.split(key).join(value);
        });
        // Σ\n   x\n   ¯\n  \n\n \n\n  Σ\n   x\n   ¯
    const regexCapital = /(\n\s*)*X(\n\s*)*¯(\n\s*)*X(\n\s*)*¯(\n\s*)*/g;
    text = text.replace(regexCapital, "$\\bar{X}$");

    const regexLower = /(\n\s*)*x(\n\s*)*¯(\n\s*)*x(\n\s*)*¯(\n\s*)*/g;
    text = text.replace(regexLower, "$\\bar{x}$");

    text = text.replace(/(\n\s*)*X(\n\s*)*¯(\n\s*)*/g, "$\\bar{X}$");
    text = text.replace(/(\n\s*)*x(\n\s*)*¯(\n\s*)*/g, "$\\bar{x}$");

    Object.entries(endReplacements)
        .sort((a, b) => b[0].length - a[0].length)
        .forEach(([key, value]) => {
            text = text.split(key).join(value);
        });

    text = text.replace(/[ \t]*\n[ \t]*/g, "\n");
    text = text.replace(/\n{3,}/g, "\n\n");
    return text.trim();
};
