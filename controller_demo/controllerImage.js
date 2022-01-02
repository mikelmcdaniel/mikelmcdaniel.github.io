class ControllerImage {
  // slotNames and slotValues are used to map to files.
  // slotValues specifies which types of things can go in that slot.
  slotNames = ["1", "2", "3", "4"];
  slotValues = [
    ["DP", "FB", "JS"],
    ["DP", "FB", "JS"],
    ["DP", "FB", "JS"],
    ["DP", "FB", "JS"]];
  // TODO: It would be nice if these didn't need to be hard-coded...
  // slotCoords and maxSlotRadius are used for mapping a 2d point to
  // the nearest slot (for UI purposes).
  slotCoords = [
    { x: 336, y: 154 },
    { x: 336, y: 334 },
    { x: 520, y: 456 },
    { x: 766, y: 372 }];
  maxSlotRadius = 150;

  // Stateful UI
  // selectedSlot is null when no slot is selected.
  // Any functions using selectedSlot should handle null!
  selectedSlot = null;

  div = null;
  baseImg = null;
  slotImgs = null;
  slotIndices = null;

  constructor(divID) {
    this.div = document.getElementById(divID);
    this.baseImg = document.getElementById(divID + ".baseImg");

    // Initialize slot info from HTML.
    this.slotImgs = [];
    this.slotIndices = [];
    for (let sni = 0; sni < this.slotNames.length; ++sni) {
      let img = document.getElementById(this.div.id + ".img" + sni);
      this.slotImgs.push(img);
      let indices = this.indicesFromImgSrc(img.src);
      console.assert(indices.slotNameIndex == sni);
      this.slotIndices.push(indices.slotValueIndex);
    }
  }

  imgSrc(slotNameIndex, slotValueIndex) {
    return this.slotValues[slotNameIndex][slotValueIndex] + this.slotNames[slotNameIndex] + ".png";
  }

  indicesFromImgSrc(imgSrc) {
    const url = new URL(imgSrc);
    const urlParts = url.pathname.split("/");
    const baseName = urlParts[urlParts.length - 1];
    // TODO: This could be more efficient!
    for (let sni = 0; sni < this.slotValues.length; ++sni) {
      for (let svi = 0; svi < this.slotValues[sni].length; ++svi) {
        if (this.imgSrc(sni, svi) == baseName) {
          return { slotNameIndex: sni, slotValueIndex: svi };
        }
      }
    }
    throw new RangeError("Could not determine slots for " + imgSrc);
  }

  closestSlot(pixelX, pixelY) {
    let slotIndex = 0;
    let closestDistance = Infinity;
    for (let sni = 0; sni < this.slotCoords.length; ++sni) {
      const cx = this.slotCoords[sni].x;
      const cy = this.slotCoords[sni].y;
      const d = Math.sqrt(Math.pow(pixelX - cx, 2) + Math.pow(pixelY - cy, 2));
      if (d < closestDistance) {
        slotIndex = sni;
        closestDistance = d;
      }
    }
    return closestDistance <= this.maxSlotRadius ? slotIndex : null;
  }

  // Change what's in a given slot.
  // e.g. incrementSlotValue(0) might change slot 0 from a D-Pad to a Joy Stick.
  incrementSlotValue(slotNameIndex) {
    if (slotNameIndex === null) {
      return;
    }
    this.slotIndices[slotNameIndex] = (this.slotIndices[slotNameIndex] + 1) % this.slotValues[slotNameIndex].length;
    this.slotImgs[slotNameIndex].src = this.imgSrc(slotNameIndex, this.slotIndices[slotNameIndex]);
  }

  decrementSlotValue(slotNameIndex) {
    if (slotNameIndex === null) {
      return;
    }
    this.slotIndices[slotNameIndex] = (this.slotIndices[slotNameIndex] + this.slotValues[slotNameIndex].length - 1) % this.slotValues[slotNameIndex].length;
    this.slotImgs[slotNameIndex].src = this.imgSrc(slotNameIndex, this.slotIndices[slotNameIndex]);
  }

  pixelCoordsFromMouseEvent(event) {
    // Modified from https://stackoverflow.com/a/58568016/5673832
    let bounds = this.baseImg.getBoundingClientRect();
    let x = event.clientX - bounds.left;
    let y = event.clientY - bounds.top;
    let scaleFactor = getComputedStyle(this.div).getPropertyValue('--scaleFactor');
    let cw = this.baseImg.clientWidth * scaleFactor;
    let ch = this.baseImg.clientHeight * scaleFactor;
    let iw = this.baseImg.naturalWidth;
    let ih = this.baseImg.naturalHeight;
    let px = Math.round(x / cw * iw);
    let py = Math.round(y / ch * ih);
    return { x: px, y: py };
  }

  //
  // Stateful UI
  //

  highlightSelectedSlot() {
    if (this.selectedSlot === null) {
      for (let sni = 0; sni < this.slotImgs.length; ++sni) {
        this.slotImgs[sni].style.opacity = 1.0;
      }
    } else {
      for (let sni = 0; sni < this.slotImgs.length; ++sni) {
        this.slotImgs[sni].style.opacity = 0.5;
      }
      this.slotImgs[this.selectedSlot].style.opacity = 1.0;
    }
  }

  setSelectedSlot(selectedSlotIndex) {
    this.selectedSlot = selectedSlotIndex;
    this.highlightSelectedSlot();
  }

  incrementSelectedSlotValue() {
    this.incrementSlotValue(this.selectedSlot);
  }

  decrementSelectedSlotValue() {
    this.decrementSlotValue(this.selectedSlot);
  }

  incrementSelectedSlot() {
    this.setSelectedSlot((this.selectedSlot + 1) % this.slotNames.length)
  }

  decrementSelectedSlot() {
    const numSlots = this.slotNames.length
    this.setSelectedSlot((this.selectedSlot + numSlots - 1) % numSlots)
  }

  //
  // Event Handlers
  //

  static onClick(self, event) {
    const coords = self.pixelCoordsFromMouseEvent(event);
    self.setSelectedSlot(self.closestSlot(coords.x, coords.y));
    self.incrementSelectedSlotValue();
  }

  static onWheel(self, event) {
    // TODO: Take the wheel/scroll amount into account...
    const coords = self.pixelCoordsFromMouseEvent(event);
    const slotIndex = self.closestSlot(coords.x, coords.y);
    self.setSelectedSlot(slotIndex);
    self.incrementSelectedSlotValue();
    if (slotIndex !== null) {
      event.preventDefault();
    }
  }

  static onMouseLeave(self, event) {
    self.setSelectedSlot(null);
  }

  static onMouseMove(self, event) {
    // TODO: Take the wheel/scroll amount into account...
    const coords = self.pixelCoordsFromMouseEvent(event);
    self.setSelectedSlot(self.closestSlot(coords.x, coords.y));
  }

  static onKeyDown(self, event) {
    const k = event.key;
    if (k == " " || k == "Enter" || k == "ArrowDown" || k == "s") {
      self.incrementSelectedSlotValue();
      event.preventDefault();
    } else if (k == "ArrowUp" || k == "w") {
      self.decrementSelectedSlotValue();
      event.preventDefault();
    } else if (k == "ArrowLeft" || (k == "Tab" && event.shiftKey) || k == "a") {
      self.decrementSelectedSlot();
      event.preventDefault();
    } else if (k == "ArrowRight" || (k == "Tab" && !event.shiftKey) || k == "d") {
      self.incrementSelectedSlot();
      event.preventDefault();
    }
  }
}

let controllerImage = new ControllerImage("controllerImageDiv");
controllerImage.div.onmousedown = function (event) { ControllerImage.onClick(controllerImage, event); }
controllerImage.div.onwheel = function (event) { ControllerImage.onWheel(controllerImage, event); }
controllerImage.div.onmouseleave = function (event) { ControllerImage.onMouseLeave(controllerImage, event); }
controllerImage.div.onmousemove = function (event) { ControllerImage.onMouseMove(controllerImage, event); }
controllerImage.div.onkeydown = function (event) { ControllerImage.onKeyDown(controllerImage, event); }
