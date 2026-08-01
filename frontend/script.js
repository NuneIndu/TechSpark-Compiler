const output = document.getElementById("output");
const codeArea = document.getElementById("code");
const inputContainer = document.getElementById("input-container");

/* ===========================
   AUTO INDENTATION
=========================== */

codeArea.addEventListener("keydown", function (e) {

    // TAB
    if (e.key === "Tab") {

        e.preventDefault();

        const start = this.selectionStart;
        const end = this.selectionEnd;

        this.value =
            this.value.substring(0, start) +
            "    " +
            this.value.substring(end);

        this.selectionStart = this.selectionEnd = start + 4;
    }

    // ENTER
    if (e.key === "Enter") {

        e.preventDefault();

        const start = this.selectionStart;

        const before = this.value.substring(0, start);
        const after = this.value.substring(start);

        const lineStart = before.lastIndexOf("\n") + 1;
        const currentLine = before.substring(lineStart);

        let indent = currentLine.match(/^\s*/)[0];

        const trimmed = currentLine.trim();

        if (trimmed.endsWith("{") || trimmed.endsWith(":")) {
            indent += "    ";
        }

        this.value = before + "\n" + indent + after;

        this.selectionStart =
        this.selectionEnd =
            start + indent.length + 1;
    }

});


/* ===========================
   AUTO SHOW INPUT BOX
=========================== */

function detectInputRequirement() {

    const code = codeArea.value;

    const patterns = [

        /input\s*\(/i,
        /scanf\s*\(/i,
        /cin\s*>>/i,
        /Scanner/i,
        /nextInt\s*\(/i,
        /nextLine\s*\(/i,
        /nextDouble\s*\(/i,
        /nextFloat\s*\(/i,
        /nextLong\s*\(/i,
        /next\s*\(/i

    ];

    const requiresInput =
        patterns.some(pattern => pattern.test(code));

    inputContainer.style.display =
        requiresInput ? "block" : "none";
}

// Detect while typing
codeArea.addEventListener("input", detectInputRequirement);


/* ===========================
   RUN CODE
=========================== */

async function runCode() {

    const language =
        document.getElementById("language").value;

    const code =
        document.getElementById("code").value;

    const input =
        document.getElementById("input").value;

    output.textContent = "Compiling...";

    try {

        const response = await fetch(
            "https://streets-nat-glen-passengers.trycloudflare.com",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    language,
                    code,
                    input
                })
            }
        );

        if (!response.ok) {
            throw new Error("Server Error : " + response.status);
        }

        const data = await response.json();

        if (data.success) {

            output.textContent = data.output;

        } else {

            output.textContent = data.error;

        }

    }

    catch (err) {

        console.error(err);

        output.textContent =
            "Error : " + err.message;

    }

}


/* ===========================
   CLEAR
=========================== */

function clearEditor() {

    codeArea.value = "";

    document.getElementById("input").value = "";

    output.textContent =
        "Program output will appear here...";

    detectInputRequirement();

}


/* ===========================
   LANGUAGE TEMPLATE
=========================== */

document
.getElementById("language")
.addEventListener("change", function () {

    let lang = this.value;

    if (lang === "java") {

        codeArea.value =
`import java.util.*;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        

    }

}`;

    }

    else if (lang === "python") {

        codeArea.value =
`name = input()

print("Hello", name)`;

    }

    else if (lang === "c") {

        codeArea.value =
`#include <stdio.h>

int main() {

    

    return 0;

}`;

    }

    else if (lang === "cpp") {

        codeArea.value =
`#include <iostream>

using namespace std;

int main() {

    

    return 0;

}`;

    }

    // Show/Hide input box after template changes
    detectInputRequirement();

});


/* ===========================
   INITIAL STATE
=========================== */

detectInputRequirement();