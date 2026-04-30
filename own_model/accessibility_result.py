class AccessibilityResult:
    def __init__(self, distance, travelTime):
        self.distance = distance
        self.travelTime = travelTime
        self.accessibilityLevel = ""

    def classifyAccessibility(self):
        if self.distance < 1.0:
            self.accessibilityLevel = "High"
        elif self.distance < 3.0:
            self.accessibilityLevel = "Moderate"
        else:
            self.accessibilityLevel = "Low"
        return self.accessibilityLevel