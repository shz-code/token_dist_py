let scanBtn = document.getElementById("scan_btn"),
    stopBtn = document.getElementById("stop_btn"),
    bar_code = document.querySelector("#barcode"),
    validityCheck = document.querySelector(".validity_check"),
    barcodeRes = document.querySelector("#barcode_res");

bar_code.style.display = "none";
const quaggaInit = () => {
    Quagga.init(
        {
            inputStream: {
                type: "LiveStream",
                constraints: {
                    width: 640,
                    height: 360,
                    facingMode: "environment",
                },
            },
            frequency: 1,
            locator: {
                patchSize: "medium",
                halfSample: true,
            },
            numOfWorkers: navigator.hardwareConcurrency
                ? navigator.hardwareConcurrency
                : 4,
            decoder: {
                readers: [
                    "code_128_reader",
                    "ean_reader",
                    "ean_8_reader",
                    "code_39_reader",
                    "code_39_vin_reader",
                    "codabar_reader",
                    "upc_reader",
                    "upc_e_reader",
                    "i2of5_reader",
                ],
                debug: {
                    showCanvas: true,
                    showPatches: true,
                    showFoundPatches: true,
                    showSkeleton: true,
                    showLabels: true,
                    showPatchLabels: true,
                    showRemainingPatchLabels: true,
                    boxFromPatches: {
                        showTransformed: true,
                        showTransformedBox: true,
                        showBB: true,
                    },
                },
            },
        },
        function (err) {
            if (err) {
                document.getElementById("v").innerHTML = err;
                return;
            }
            document.getElementById("v").innerHTML =
                "Initialization finished. Ready to start";
            Quagga.start();
        }
    );
};


scanBtn.addEventListener("click", () => {
    let status = scanBtn.getAttribute("data-status");
    if (status === "false") {
        document.getElementById("interactive").style.display = "block";
        quaggaInit();
        scanBtn.setAttribute("data-status", "true");
    }
});

stopBtn.addEventListener("click", () => {
    let status = scanBtn.getAttribute("data-status");
    if (status === "true") {
        Quagga.stop();
        scanBtn.setAttribute("data-status", "false");
        document.getElementById("interactive").style.display = "none";
    }
});

const check_barcode = () =>{
    let code = validityCheck.getAttribute("code");
    console.log(code);
}

Quagga.onDetected(function (result) {
    document.getElementById("v").innerHTML = result.codeResult.code;
    bar_code.style.display = "block";
    JsBarcode("#barcode", `${result.codeResult.code}`);
    validityCheck.classList.add("show");
    validityCheck.setAttribute("code",result.codeResult.code);
    barcodeRes.innerHTML = result.codeResult.code
});