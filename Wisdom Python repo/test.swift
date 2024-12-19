/*
 Copyright (C) 2016 Apple Inc. All Rights Reserved.
 See LICENSE.txt for this sample’s licensing information
 
 Abstract:
 This application's view controller.
 */

import UIKit
import WatchConnectivity
import os.log
import CoreML
import DGCharts
import Foundation

class ViewController: UIViewController, ChartViewDelegate, UITextFieldDelegate {
    
    let appDelegate = UIApplication.shared.delegate as! AppDelegate
  
    var session: WCSession?
    //MARK: ViewController variables
    
    // IBOutlets to connect code to storyboard layout
    @IBOutlet weak var StatusLabel: UILabel!
    @IBOutlet weak var shotlabel: UILabel!
    @IBOutlet weak var classlabel: UILabel!
    @IBOutlet weak var pieChartshots: PieChartView!
    @IBOutlet weak var lineChart: LineChartView!
    @IBOutlet weak var segmentedcontrol: UISegmentedControl!
    @IBOutlet weak var textfield: UITextField!
    @IBOutlet weak var Shot_Quality: UILabel!
    @IBOutlet weak var Follow_through: UILabel!
    
    var backhandDataEntry = PieChartDataEntry(value: 0)
    var foreDataEntry = PieChartDataEntry(value: 0)
    var serveDataEntry = PieChartDataEntry(value: 0)
    var forevDataEntry = PieChartDataEntry(value: 0)
    var backvDataEntry = PieChartDataEntry(value: 0)
    
    var numberOfDownloadsDataEntries = [PieChartDataEntry]()
    var line_entries = [BarChartDataEntry]()
    
    var count = 0
    var readFile = ""
    var graph = 0
    var status = true
    
//    var template_serve = [String]()
    
    var gravityX = [Double]()
    var gravityY = [Double]()
    var gravityZ = [Double]()
    var shotlength = 249
    let sensorfreq = 100.0
    
    
    struct Template {
        
        var accX_template: String = ""
        var accY_template: String = ""
        var accZ_template: String = ""
        var rotX_template: String = ""
        var rotY_template: String = ""
        var rotZ_template: String = ""
        
        init(raw: [String]) {
            
            accX_template = raw[0]
            accY_template = raw[1]
            accZ_template = raw[2]
            rotX_template = raw[3]
            rotY_template = raw[4]
            rotZ_template = raw[5]
            
        }
    }
    

    
    //MARK: CreateML framework set-up
    
    // Define some ML Model constants for the recurrent network
      struct ModelConstants {
        static let numOfFeatures = 6
        // Must be the same value you used while training
        static let predictionWindowSize = 250
        static let sensorsUpdateFrequency = 1.0 / 100.0
        static let hiddenInLength = 20
        static let hiddenCellInLength = 380
      }
    // Initialize the model, layers, and sensor data arrays
      private let classifier = SVM_ver2_5Class()
      private let modelName:String = "SVM_ver2_5Class()"
    
    private let quality_class = Randf_Serve_Quality()
    private let quality_modelname:String = "Randf_Serve_Quality"
    
    
    
    var temp_serve_xg = [String]()
    

//    let accX_final = try? MLMultiArray(
//        shape: [ModelConstants.predictionWindowSize] as [NSNumber],
//        dataType: MLMultiArrayDataType.double)
//    let accY_final = try? MLMultiArray(
//        shape: [ModelConstants.predictionWindowSize] as [NSNumber],
//        dataType: MLMultiArrayDataType.double)
//    let accZ_final = try? MLMultiArray(
//        shape: [ModelConstants.predictionWindowSize] as [NSNumber],
//        dataType: MLMultiArrayDataType.double)
//    let rotX_final = try? MLMultiArray(
//        shape: [ModelConstants.predictionWindowSize] as [NSNumber],
//        dataType: MLMultiArrayDataType.double)
//    let rotY_final = try? MLMultiArray(
//        shape: [ModelConstants.predictionWindowSize] as [NSNumber],
//        dataType: MLMultiArrayDataType.double)
//    let rotZ_final = try? MLMultiArray(
//        shape: [ModelConstants.predictionWindowSize] as [NSNumber],
//        dataType: MLMultiArrayDataType.double)
//    var currentState = try? MLMultiArray(
//        shape: [(ModelConstants.hiddenInLength +
//          ModelConstants.hiddenCellInLength) as NSNumber],
//        dataType: MLMultiArrayDataType.double)
    

    
    //MARK: Set Up

    override func viewDidLoad() 
    {
        super.viewDidLoad()
        
        pieChartshots.delegate = self
        lineChart.delegate = self
        
        textfield.delegate = self
        
        self.configureWatchKitSession()
        
        updateChartData()
        
        let bottomline = CALayer()
        
        bottomline.frame = CGRect(x: 0, y: textfield.frame.height, width: textfield.frame.width, height: 2)
        
        bottomline.backgroundColor = UIColor.init(red: 48/255, green: 173/255, blue: 99/255, alpha: 1).cgColor
        
        textfield.borderStyle = .none
        textfield.layer.addSublayer(bottomline)
        
        
    }
    
    // Configure Watch Connection
    func configureWatchKitSession() {

    if WCSession.isSupported() {
      session = WCSession.default
      session?.delegate = self
      session?.activate()
    }
    }
    
    
    //MARK: Chart Functions
    
    
    func updateLineChart(line_entries: [BarChartDataEntry], name: String) {
        
        let set2 = LineChartDataSet(entries: line_entries, label: name)
        set2.colors = [NSUIColor(red: CGFloat(80.0/255), green: CGFloat(33.0/255), blue: CGFloat(222.0/255), alpha: 1)]
        self.lineChart.legend.verticalAlignment = .top
        self.lineChart.legend.horizontalAlignment = .left
        set2.drawCirclesEnabled = false;
        set2.lineWidth = 5.5
        set2.drawValuesEnabled = false
        
        
        let data2 = LineChartData(dataSet: set2)
        lineChart.data = data2
        lineChart.noDataText = "You need to register a shot for this chart to display!"
//        lineChart.backgroundColor = UIColor(red: 189/255, green: 195/255, blue: 199/255, alpha: 1)
        lineChart.animate(xAxisDuration: 2.0, yAxisDuration: 2.0, easingOption: .easeInBounce)
        lineChart.drawMarkers = false
        lineChart.rightAxis.enabled = false
        lineChart.xAxis.labelPosition = .bottom
        lineChart.xAxis.drawLabelsEnabled = true
        
    }
    
    
    func updateChartData() {
        
        var counts: [String: Int] = [:]
        appDelegate.shots.forEach { counts[$0, default: 0] += 1 }
        
        var names = [String]()
        var values = [Int]()
        
        for (key, value) in counts {
            names.append(key)
            values.append(value)
        }
        
        pieChartshots.chartDescription.text = ""
        pieChartshots.noDataText = "You need to register a shot for this chart to display!"
        
        backhandDataEntry.label = "backhand"
        let back_index = names.enumerated().filter{ $0.element == "backhand"}.map{ $0.offset }
        if back_index.count > 0 {
            let val_back  = Double(values[back_index[0]])
            backhandDataEntry.value = val_back
        }
        else {backhandDataEntry.value = 0}
        
        foreDataEntry.label = "forehand"
        let fore_index = names.enumerated().filter{ $0.element == "forehand"}.map{ $0.offset }
        if fore_index.count > 0 {
            let val_fore  = Double(values[fore_index[0]])
            foreDataEntry.value = val_fore
        }
        else {foreDataEntry.value = 0}
        
        serveDataEntry.label = "serve"
        let serve_index = names.enumerated().filter{ $0.element == "serve"}.map{ $0.offset }
        if serve_index.count > 0 {
            let val_serve  = Double(values[serve_index[0]])
            serveDataEntry.value = val_serve
        }
        else {serveDataEntry.value = 0}

        forevDataEntry.label = "volley forehand"
        let forev_index = names.enumerated().filter{ $0.element == "volley forehand"}.map{ $0.offset }
        if forev_index.count > 0 {
            let val_forev  = Double(values[forev_index[0]])
            forevDataEntry.value = val_forev
        }
        else {forevDataEntry.value = 0}

        backvDataEntry.label = "volley backhand"
        let backv_index = names.enumerated().filter{ $0.element == "volley backhand"}.map{ $0.offset }
        if backv_index.count > 0 {
            let val_backv  = Double(values[backv_index[0]])
            backvDataEntry.value = val_backv
        }
        else {backvDataEntry.value = 0}

        
        numberOfDownloadsDataEntries = [backhandDataEntry, foreDataEntry, serveDataEntry, forevDataEntry, backvDataEntry]
        
        let chartDataSet = PieChartDataSet(entries: numberOfDownloadsDataEntries)
        let chartData = PieChartData(dataSet: chartDataSet)
        
        self.pieChartshots.legend.enabled = false
        chartDataSet.colors = ChartColorTemplates.joyful()
        chartDataSet.valueTextColor=NSUIColor(red: 0/255.0, green: 0/255.0, blue: 0/255.0, alpha: 1.0)
        pieChartshots.data = chartData
        pieChartshots.animate(xAxisDuration: 2.0, yAxisDuration: 2.0, easingOption: .easeInBounce)
        
    }
// Mark: Check that data ahs been recorded so app doesnt crash when trying to retrieve it
    
    func checkData() -> Bool
    {
        var session_active: Bool
        if count == 1 {
            session_active = false
        }else{
           session_active = true
        }
    return session_active
    }
    
    //MARK: UI Button Functions

    
    @IBAction func displayXAcc(_ sender: Any) {
        
        if checkData() {
            var line = [BarChartDataEntry]()
            for x in 0...shotlength {
                line.append(BarChartDataEntry(x: Double(x)/sensorfreq, y: appDelegate.accX_edit[x]))
            }
            updateLineChart(line_entries: line, name: "X Acceleration")
        }
    }
    @IBAction func displayYAcc(_ sender: Any) {
        if checkData() {
            var line = [BarChartDataEntry]()
            for x in 0...shotlength {
                line.append(BarChartDataEntry(x: Double(x)/sensorfreq, y: appDelegate.accY_edit[x]))
            }
            updateLineChart(line_entries: line, name: "Y Acceleration")
        }
    }
    @IBAction func displayZAcc(_ sender: Any) {
        if checkData() {
            var line = [BarChartDataEntry]()
            for x in 0...shotlength {
                line.append(BarChartDataEntry(x: Double(x)/sensorfreq, y: appDelegate.accZ_edit[x]))
            }
            updateLineChart(line_entries: line, name: "Z Acceleration")
        }
    }
    @IBAction func displayXGyro(_ sender: Any) {
        if checkData() {
            var line = [BarChartDataEntry]()
            for x in 0...shotlength {
                line.append(BarChartDataEntry(x: Double(x)/sensorfreq, y: appDelegate.rotX_edit[x]))
            }
            updateLineChart(line_entries: line, name: "X Rotation")
        }
    }
    @IBAction func displayYGyro(_ sender: Any) {
        if checkData() {
            var line = [BarChartDataEntry]()
            for x in 0...shotlength {
                line.append(BarChartDataEntry(x: Double(x)/sensorfreq, y: appDelegate.rotY_edit[x]))
            }
            updateLineChart(line_entries: line, name: "Y Rotation")
        }
    }
    @IBAction func displayZGyro(_ sender: Any) {
        if checkData() {
            var line = [BarChartDataEntry]()
            for x in 0...shotlength {
                line.append(BarChartDataEntry(x: Double(x)/sensorfreq, y: appDelegate.rotZ_edit[x]))
            }
            updateLineChart(line_entries: line, name: "Z Rotation")
        }
    }
    
    
    
    @IBAction func orientationtoggle(_ sender: Any) {
        
        switch segmentedcontrol.selectedSegmentIndex
        {
        case 0:
            appDelegate.orientation[appDelegate.session_no] = "Right Handed"
        case 1:
            appDelegate.orientation[appDelegate.session_no] = "Left Handed"
        default:
            break
        }
        
    }

    
    @IBAction func SaveSession(_ sender: Any) {
        
        let date = Date()
        let formatter1 = DateFormatter()
        formatter1.dateFormat = "HH:mm E, d MMM y"
        print(formatter1.string(from: date))
        appDelegate.endtimes.append(formatter1.string(from: date))
    

        let c = Double(appDelegate.shots.count)
        
        if appDelegate.percentaccuracy > 0.0 {
            let acc = Double((Double(appDelegate.percentaccuracy/c))*100.0)
            print(acc)
            appDelegate.overallaccuracy.append(Double(acc))
        }
        else {appDelegate.overallaccuracy.append(0.0)}
        
        status = true
        
        
        let image = pieChartshots.getChartImage(transparent: false)!
        let string = image.toPngString() // it will convert UIImage to string
        appDelegate.image.append(string!)
        
        
        if appDelegate.shots.count > 0 {
            appDelegate.session_no += 1
        }
        
        print(appDelegate.session_no)
        print(appDelegate.starttimes)
        
        appDelegate.stats.removeAll()
        appDelegate.accX_graph.removeAll()
        appDelegate.accY_graph.removeAll()
        appDelegate.accZ_graph.removeAll()
        appDelegate.rotX_graph.removeAll()
        appDelegate.rotY_graph.removeAll()
        appDelegate.rotZ_graph.removeAll()
        
        appDelegate.shots.removeAll()
        print(appDelegate.shots)
        
        appDelegate.firstclick = true
        
        appDelegate.name.append(textfield.text!)
        print(appDelegate.name)
        
        
        updateChartData()
        self.shotlabel.text = String(0)
        
        if let validSession = self.session, validSession.isReachable {
            print("Hello")
          let data: [String: Any] = ["iPhone": "Data from iPhone" as Any] // Create your Dictionay as per uses
          validSession.sendMessage(data, replyHandler: nil, errorHandler: { error in
              // catch any errors here
              print(error)
              
              }
          )}
        
    }
    


    //MARK: Predicition Functions
    
    func activityPrediction() {
        
//        print (readFile)
//        print(readFile.count)
        
        let sep = readFile.components(separatedBy: ",")
//        print(sep.count)
        

        if (sep.count > 1400) {
            // 250 here referes to amount of samples in a shot to be fed
            // to the model
            let rotX = sep[1...250]
            let rotY = sep[253...502]
            let rotZ = sep[505...754]
            let accX = sep[757...1006]
            let accY = sep[1009...1258]
            let accZ = sep[1261...1510]
            let gravX = sep[1513...1762]
            let gravY = sep[1765...2014]
            let gravZ = sep[2017...2266]
            let roll = sep[2269...2518]
            let pitch = sep[2521...2770]
            let yaw = sep[2773...3022]

            appDelegate.rotX_edit = rotX.doubleArray
            appDelegate.rotY_edit = rotY.doubleArray
            appDelegate.rotZ_edit = rotZ.doubleArray
            appDelegate.accX_edit = accX.doubleArray
            appDelegate.accY_edit = accY.doubleArray
            appDelegate.accZ_edit = accZ.doubleArray
            appDelegate.pitch_edit = pitch.doubleArray
            appDelegate.roll_edit = roll.doubleArray
            appDelegate.yaw_edit = yaw.doubleArray
            
            
            gravityX = gravX.doubleArray
            gravityY = gravY.doubleArray
            gravityZ = gravZ.doubleArray
            
    
//            for j in (0...249) {
//                self.rotX_final![j] = appDelegate.rotX_edit[j] as NSNumber
//                self.rotY_final![j] = appDelegate.rotY_edit[j] as NSNumber
//                self.rotZ_final![j] = appDelegate.rotZ_edit[j] as NSNumber
//                self.accX_final![j] = appDelegate.accX_edit[j] as NSNumber
//                self.accY_final![j] = appDelegate.accY_edit[j] as NSNumber
//                self.accZ_final![j] = appDelegate.accZ_edit[j] as NSNumber
//            }
//            
//            print(rotX_final as Any)
//            
            appDelegate.rotX_graph.append(appDelegate.rotX_edit)
            appDelegate.rotY_graph.append(appDelegate.rotY_edit)
            appDelegate.rotZ_graph.append(appDelegate.rotZ_edit)
            appDelegate.accX_graph.append(appDelegate.accX_edit)
            appDelegate.accY_graph.append(appDelegate.accY_edit)
            appDelegate.accZ_graph.append(appDelegate.accZ_edit)
            
            PerformanceParameters()
            
            graph = graph + 1
            
//
            
        }
    }
    


    func calculateStats(data: [Double]) -> (min: Double, max: Double, stdDev: Double, area: Double, mean: Double) {
        //         calculate min max, area and std deviation of the values of gyro and acceleration
        let min = data.min() ?? 0
        let max = data.max() ?? 0
        
        let mean = data.reduce(0, +) / Double(data.count)
        let sumOfSquares = data.map { pow($0 - mean, 2) }.reduce(0, +)
        let stdDev = sqrt(sumOfSquares / Double(data.count))
        
        var area = 0.0
        for i in data.indices.dropLast() {
            area += (data[i] + data[i + 1]) / 2.0
        }
//        print(min, max, stdDev, area, mean)
        return (min, max, stdDev, area, mean)
    }
    
    func QualityPrediction(gxmin: Double,gymin: Double, gzmin: Double ,gzmax: Double,gymean: Double, gyarea: Double,gzarea: Double) -> String? {

        let QualityPred = try? quality_class.prediction(Gyro_x_min: gxmin, Gyro_y_min: gymin, Gyro_z_min: gzmin, Gyro_z_max: gzmax, Gyro_y_mean: gymean, Gyro_y_area: gyarea, Gyro_z_area: gzarea)
        let qual = QualityPred?.Quality
        self.Shot_Quality.text = qual!
        print(qual)
        return QualityPred?.Quality
        
    }
    func Quality_stats_serve(){
        var ydata = appDelegate.accY_edit
        var zdata = appDelegate.accZ_edit
        let gxmin = appDelegate.accX_edit[100...140].min() ?? 0
        let gymin = ydata[100...140].min() ?? 0
        let gzmin = zdata[100...140].min() ?? 0
        let gzmax = zdata[140...200].max() ?? 0
        let gymean = ydata.reduce(0, +) / Double(ydata.count)
        var gyarea = 0.0
        let ydata_sub = ydata[125...249]
        for i in ydata_sub.indices.dropLast() {
            gyarea += (ydata_sub[i] + ydata_sub[i + 1]) / 2.0
        }
        let zdata_sub = zdata[130...170]
        var gzarea = 0.0
        for i in zdata_sub.indices.dropLast() {
            gzarea += (zdata_sub[i] + zdata_sub[i + 1]) / 2.0
        
        }
        QualityPrediction(gxmin: gxmin, gymin: gymin, gzmin: gzmin,gzmax:gzmax, gymean: gymean, gyarea: gyarea, gzarea: gzarea)

    }
    func activityPrediction2() -> String? {

   
        let (accel_x_min, accel_x_max, accel_x_stdDev, accel_x_area,accel_x_mean) = calculateStats(data: appDelegate.accX_edit)
        
        let (accel_y_min, accel_y_max, accel_y_stdDev, accel_y_area,accel_y_mean) = calculateStats(data: appDelegate.accY_edit)
        
        let (accel_z_min, accel_z_max, accel_z_stdDev, accel_z_area,accel_z_mean) = calculateStats(data: appDelegate.accZ_edit)
        
        let (gyrox_min, gyrox_max, gyrox_stdDev, gyrox_area,gyrox_mean) = calculateStats(data: appDelegate.rotX_edit)
        
        let (gyroy_min, gyroy_max, gyroy_stdDev, gyroy_area,gyroy_mean) = calculateStats(data: appDelegate.rotY_edit)
        
        let (gyroz_min,gyroz_max,gyroz_stdDev,gyroz_area,gyroz_mean) = calculateStats(data: appDelegate.rotZ_edit)
        
              // Create the input for the model
        let modelPrediction = try? classifier.prediction(acceleration_x_max: accel_x_max, acceleration_y_max: accel_y_max, acceleration_z_max: accel_z_max, acceleration_x_min: accel_x_min, acceleration_y_min: accel_y_min, acceleration_z_min: accel_z_min, acceleration_x_mean: accel_x_mean, acceleration_y_mean: accel_y_mean, acceleration_z_mean: accel_z_mean, acceleration_x_std: accel_x_stdDev, acceleration_y_std: accel_y_stdDev, acceleration_z_std: accel_z_stdDev, acceleration_x_area: accel_x_area, acceleration_y_area: accel_y_area, acceleration_z_area: accel_z_area, gyro_x_min: gyrox_min, gyro_y_min: gyroy_min, gyro_z_min: gyroz_min, gyro_x_max: gyrox_max, gyro_y_max: gyroy_max, gyro_z_max: gyroz_max, gyro_x_mean: gyrox_mean, gyro_y_mean: gyroy_mean, gyro_z_mean: gyroz_mean, gyro_x_std: gyrox_stdDev, gyro_y_std: gyroy_stdDev, gyro_z_std: gyroz_stdDev, gyro_x_area: gyrox_area, gyro_y_area: gyroy_area, gyro_z_area: gyroz_area)
    // Return the predicted activity
        let pred = modelPrediction?.shot_type
        self.classlabel.text = pred!
        print(pred!)
        if pred == "serve" {
            Quality_stats_serve()
            if let validSession = self.session, validSession.isReachable {
                print("bye")
                let data: [String: Any] = ["shot_quality": self.Shot_Quality.text as Any] // Create your Dictionay as per uses
                validSession.sendMessage(data, replyHandler: nil, errorHandler: { error in
                    // catch any errors here
                    print(error)
                }
                )}
        }
        
        if let validSession = self.session, validSession.isReachable {
            print("Hello")
          let data: [String: Any] = ["shotType": pred as Any] // Create your Dictionay as per uses
          validSession.sendMessage(data, replyHandler: nil, errorHandler: { error in
              // catch any errors here
              print(error)
              
              }
          )}

        return modelPrediction?.shot_type
    }
    
    
    // This function is called when you click return key in the text field.
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        
        print("textFieldShouldReturn")
        
        // Resign the first responder from textField to close the keyboard.
        textField.resignFirstResponder()
        

        
        
        return true
    }
    
    
    func standardizeSignal(_ signal: [Double]) -> [Double] {
                 let mean = signal.reduce(0, +) / Double(signal.count)
                 let stdDev = sqrt(signal.map { pow($0 - mean, 2) }.reduce(0, +) / Double(signal.count))
                 return signal.map { ($0 - mean) / stdDev }
             }
     
     func calculateConsistency(template: [[Double]]) -> [Double] {
          var consistency = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
         let standardizedAccX = standardizeSignal(appDelegate.accX_edit)
         let standardizedAccY = standardizeSignal(appDelegate.accY_edit)
         let standardizedAccZ = standardizeSignal(appDelegate.accZ_edit)
         let standardizedRotX = standardizeSignal(appDelegate.rotX_edit)
         let standardizedRotY = standardizeSignal(appDelegate.rotY_edit)
         let standardizedRotZ = standardizeSignal(appDelegate.rotZ_edit)
         
          for i in 0...shotlength {
              consistency[0] += pow((standardizedAccX[i] - Double((template[0].index(0, offsetBy: i)))), 2)
              consistency[1] += pow((standardizedAccY[i] - Double((template[1].index(0, offsetBy: i)))), 2)
              consistency[2] += pow((standardizedAccZ[i] - Double((template[2].index(0, offsetBy: i)))), 2)
              consistency[3] += pow((standardizedRotX[i] - Double((template[3].index(0, offsetBy: i)))), 2)
              consistency[4] += pow((standardizedRotY[i] - Double((template[4].index(0, offsetBy: i)))), 2)
              consistency[5] += pow((standardizedRotZ[i] - Double((template[5].index(0, offsetBy: i)))), 2)
          }
          
          consistency[0] = sqrt(consistency[0])/250
          consistency[1] = sqrt(consistency[1])/250
          consistency[2] = sqrt(consistency[2])/250
          consistency[3] = sqrt(consistency[3])/250
          consistency[4] = sqrt(consistency[4])/250
          consistency[5] = sqrt(consistency[5])/250
          print(consistency)
          
          return consistency
      }
    
    func PerformanceParameters() {
        
        // BAT SPEED
        let g_y_max_av = appDelegate.rotY_edit.max()!
        let g_z_max_av = appDelegate.rotZ_edit.max()!
        let omega = sqrt(pow(g_y_max_av, 2) + pow(g_z_max_av, 2))
        let RacketSpeedAverage = omega*0.769
        
        
        // SHOT QUALITY
        
        let temp_back = getCSVData(from: "Back_template")
        let temp_forehand = getCSVData(from: "Fore_template")
        let temp_serve = getCSVData(from: "Serve_template")
        let temp_backv = getCSVData(from: "BackV_template")
        let temp_forev = getCSVData(from: "ForeV_template")
        
        var temp_bck = [[Double]]()
        var temp_fre = [[Double]]()
        var temp_srv = [[Double]]()
        var temp_bckv = [[Double]]()
        var temp_frv = [[Double]]()
        
        for x in 0...5 {
            temp_bck.append(temp_back[x].doubleArray)
            temp_fre.append(temp_forehand[x].doubleArray)
            temp_srv.append(temp_serve[x].doubleArray)
            temp_bckv.append(temp_backv[x].doubleArray)
            temp_frv.append(temp_forev[x].doubleArray)
        }
        
        var consistency = [0.0,0.0,0.0,0.0,0.0,0.0]
        
        var avgconsistency = Double()
        
        if self.classlabel.text == "backhand" {
            consistency = calculateConsistency(template: temp_bck)
            print(consistency)
            consistency[0] = 10*(30-consistency[0])/26
            consistency[1] = 10*(30-consistency[1])/26
            consistency[2] = 10*(30-consistency[2])/26
            consistency[3] = 10*(30-consistency[3])/26
            consistency[4] = 10*(30-consistency[4])/26
            consistency[5] = 10*(30-consistency[5])/26
            
            let sumArray = consistency.reduce(0, +)
            avgconsistency = sumArray / Double(consistency.count)
            let current_angle = (180 / .pi) * abs(appDelegate.roll_edit[155] - appDelegate.roll_edit[120])
            self.Follow_through.text = String(current_angle)
            appDelegate.followthrough_angle.append(current_angle)
        }
        
        if self.classlabel.text == "forehand" {
            consistency = calculateConsistency(template: temp_fre)
            print(consistency)
            consistency[0] = 10*(30-consistency[0])/26
            consistency[1] = 10*(30-consistency[1])/26
            consistency[2] = 10*(30-consistency[2])/26
            consistency[3] = 10*(30-consistency[3])/26
            consistency[4] = 10*(30-consistency[4])/26
            consistency[5] = 10*(30-consistency[5])/26
            
            let sumArray = consistency.reduce(0, +)
            avgconsistency = sumArray / Double(consistency.count)
            let current_angle = (180 / .pi) * abs(appDelegate.roll_edit[155] - appDelegate.roll_edit[120])
            self.Follow_through.text = String(current_angle)
            appDelegate.followthrough_angle.append(current_angle)
        }
        
        if self.classlabel.text == "serve" {
            consistency = calculateConsistency(template: temp_srv)
            print(consistency)
            consistency[0] = 10*(30-consistency[0])/26
            consistency[1] = 10*(30-consistency[1])/26
            consistency[2] = 10*(30-consistency[2])/26
            consistency[3] = 10*(30-consistency[3])/26
            consistency[4] = 10*(30-consistency[4])/26
            consistency[5] = 10*(30-consistency[5])/26
            let sumArray = consistency.reduce(0, +)
            avgconsistency = sumArray / Double(consistency.count)
        }
        
        if self.classlabel.text == "volley forehand" {
            consistency = calculateConsistency(template: temp_frv)
            print(consistency)
            consistency[0] = 10*(30-consistency[0])/26
            consistency[1] = 10*(30-consistency[1])/26
            consistency[2] = 10*(30-consistency[2])/26
            consistency[3] = 10*(30-consistency[3])/26
            consistency[4] = 10*(30-consistency[4])/26
            consistency[5] = 10*(30-consistency[5])/26
            let sumArray = consistency.reduce(0, +)
            avgconsistency = sumArray / Double(consistency.count)
        }
        
        if self.classlabel.text == "volley backhand" {
            consistency = calculateConsistency(template: temp_bckv)
            print(consistency)
            consistency[0] = 10*(30-consistency[0])/26
            consistency[1] = 10*(30-consistency[1])/26
            consistency[2] = 10*(30-consistency[2])/26
            consistency[3] = 10*(30-consistency[3])/26
            consistency[4] = 10*(30-consistency[4])/26
            consistency[5] = 10*(30-consistency[5])/26
            let sumArray = consistency.reduce(0, +)
            avgconsistency = sumArray / Double(consistency.count)
        }
        
//        if avgconsistency < 0 {
//            avgconsistency = 0
//        }
        
        
        // Initial Bat Lift Angle
        
        let initialangles_lookup = Array(stride(from: 45.0, through: 180.0, by: 0.1))
        
        let no_init = initialangles_lookup.count
        let increment = 0.9/Double(no_init)
        
        var yvals = [Double]()
        var idx = [Double]()
        
        for x in 0...no_init {
            
            yvals.append(0.1 + Double(x)*increment)
            idx.append(abs(yvals[x] - gravityY[0]))
        }
                
        
        let value = idx.min()!
        let index = idx.firstIndex(of: value)!
        let InitialAngle = initialangles_lookup[index]


        
        // Impact Bat Lift Angle
        
        var ImpactAngle = Double()
        
        if self.classlabel.text == "backhand" {
            
            let impactangles_lookup = Array(stride(from: -10.0, through: 45.0, by: 0.1))
            let no_imp_def = impactangles_lookup.count
            let increment = 0.1/Double(no_imp_def)
            var yvals = [Double]()
            var idx = [Double]()
            
            for x in 0...no_imp_def-1 {
                yvals.append(0.9 - Double(x)*increment)
                idx.append(abs(yvals[x] - gravityY[60]))
            }
                    
            let value = idx.min()!
            let index = idx.firstIndex(of: value)!
            ImpactAngle = impactangles_lookup[index]
        }
        
        if self.classlabel.text == "forehand" {
            
            let impactangles_lookup = Array(stride(from: -45.0, through: 45.0, by: 0.1))
            let no_imp_drv = impactangles_lookup.count
            let increment = 0.1/Double(no_imp_drv)
            var yvals = [Double]()
            var idx = [Double]()
            
            for x in 0...no_imp_drv-1 {
                yvals.append(0.9 - Double(x)*increment)
                idx.append(abs(yvals[x] - gravityY[60]))
            }
                    
            let value = idx.min()!
            let index = idx.firstIndex(of: value)!
            ImpactAngle = impactangles_lookup[index]
        }
        
        
        if self.classlabel.text == "serve" {
            
            let impactangles_lookup = Array(stride(from: 45.0, through: 160.0, by: 0.1))
            let no_imp_serve = impactangles_lookup.count
            let increment = 0.4/Double(no_imp_serve)
            var yvals = [Double]()
            var idx = [Double]()
            
            for x in 0...no_imp_serve-1 {
                yvals.append(0.5 + Double(x)*increment)
                idx.append(abs(yvals[x] - gravityZ[60]))
            }
                    
            let value = idx.min()!
            let index = idx.firstIndex(of: value)!
            ImpactAngle = impactangles_lookup[index]
        }
        
        if self.classlabel.text == "volley forehand" {
            
            let impactangles_lookup = Array(stride(from: 45.0, through: 160.0, by: 0.1))
            let no_imp_pll = impactangles_lookup.count
            let increment = 0.4/Double(no_imp_pll)
            var yvals = [Double]()
            var idx = [Double]()
            
            for x in 0...no_imp_pll-1 {
                yvals.append(0.5 + Double(x)*increment)
                idx.append(abs(yvals[x] - gravityZ[60]))
            }
                    
            let value = idx.min()!
            let index = idx.firstIndex(of: value)!
            ImpactAngle = impactangles_lookup[index]
        }
        
        
        if self.classlabel.text == "volley backhand" {
            
            let impactangles_lookup = Array(stride(from: 45.0, through: 160.0, by: 0.1))
            let no_imp_swp = impactangles_lookup.count
            let increment = 0.4/Double(no_imp_swp)
            var yvals = [Double]()
            var idx = [Double]()
            
            for x in 0...no_imp_swp-1 {
                yvals.append(0.5 - Double(x)*increment)
                idx.append(abs(yvals[x] - gravityZ[60]))
            }
                    
            let value = idx.min()!
            let index = idx.firstIndex(of: value)!
            ImpactAngle = impactangles_lookup[index]
        }
        
        

        let features = [RacketSpeedAverage,avgconsistency,InitialAngle,ImpactAngle]
        appDelegate.stats.append(features)
        
    }
    
    
    func getCSVData(from csvName: String) -> [[String]] {
        
        var temp_xa = [String]()
        var temp_ya = [String]()
        var temp_za = [String]()
        var temp_xg = [String]()
        var temp_yg = [String]()
        var temp_zg = [String]()
        
        guard let filePath = Bundle.main.path(forResource: csvName, ofType: "csv") else {
            return []
        }
        
        var data = ""
        do {
            data = try String(contentsOfFile: filePath)
        } catch {
            print(error)
            return []
        }
        
        var rows = data.components(separatedBy: "\n")
        rows.removeFirst()
        
        for row in rows {
            
            let csvColumns = row.components(separatedBy: ",")
            temp_xa.append(csvColumns[0])
            temp_ya.append(csvColumns[0])
            temp_za.append(csvColumns[0])
            temp_xg.append(csvColumns[0])
            temp_yg.append(csvColumns[0])
            temp_zg.append(csvColumns[0])
        }
        
        let csvToStruct = [temp_xa, temp_ya, temp_za, temp_xg, temp_yg, temp_zg]
        
        return csvToStruct
    }


    
    // This function is called when you input text in the textView.
        func textView(_ textView: UITextView, shouldChangeTextIn range: NSRange, replacementText text: String) -> Bool{
            
            print("textView.")
            
            print("input text is : \(text)")
            
            // If user press return key in the keyboard.
            if("\n" == text){
                
                // Resign first responder from UITextView to close the keyboard.
                textView.resignFirstResponder()
                
                return false
            }
            
            return true
        }
    
    
    
    
}




//MARK: Watch Session Delegate


extension ViewController: WCSessionDelegate {
  
  func sessionDidBecomeInactive(_ session: WCSession) {}
  
  func sessionDidDeactivate(_ session: WCSession) {}
  
  func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) {}
  
  func session(_ session: WCSession, didReceiveMessage message: [String : Any]) {
//    print("received message: \(message)")
      DispatchQueue.main.async { [self] in
          if (message["watch"] as? String) != nil {
          
              self.shotlabel.text = String(0)
              

              let date = Date()
              let formatter1 = DateFormatter()
              formatter1.dateFormat = "HH:mm E, d MMM y"
//              print(formatter1.string(from: date))
              appDelegate.endtimes.append(formatter1.string(from: date))
              
              
              let image = pieChartshots.getChartImage(transparent: false)!
              let string = image.toPngString() // it will convert UIImage to string
              appDelegate.image.append(string!)
              
              appDelegate.session_no += 1
              
              appDelegate.stats.removeAll()
              appDelegate.accX_graph.removeAll()
              appDelegate.accY_graph.removeAll()
              appDelegate.accZ_graph.removeAll()
              appDelegate.rotX_graph.removeAll()
              appDelegate.rotY_graph.removeAll()
              appDelegate.rotZ_graph.removeAll()
              appDelegate.accX_edit.removeAll()
              appDelegate.accY_edit.removeAll()
              appDelegate.accZ_edit.removeAll()
              appDelegate.rotX_edit.removeAll()
              appDelegate.rotY_edit.removeAll()
              appDelegate.rotZ_edit.removeAll()
              appDelegate.shots.removeAll()
              print(appDelegate.shots)
              
              appDelegate.firstclick = true
              
              updateChartData()
              status = true
          }
          
        if let value = message["count"] as? String {
          self.shotlabel.text = value
        }
          
        if let value = message["on"] as? String {
          self.StatusLabel.text = value
            
            if status == true {
                let date = Date()
                let formatter1 = DateFormatter()
                formatter1.dateFormat = "HH:mm E, d MMM y"
//                print(formatter1.string(from: date))
                appDelegate.starttimes.append(formatter1.string(from: date))
            }
            
            appDelegate.firstclick = true
            status = false
            appDelegate.orientation.append("Right Handed")
        }
          
        if let value = message["off"] as? String {
            self.StatusLabel.text = value
          }
          
        if let value = message["array"] as? String {
            
            let fileName = "shot \(self.count)"
            let documentDirectoryUrl = try! FileManager.default.url(
               for: .documentDirectory, in: .userDomainMask, appropriateFor: nil, create: true
            )
            let fileUrl = documentDirectoryUrl.appendingPathComponent(fileName).appendingPathExtension("txt")
            // prints the file path
            print("File path \(fileUrl.path)")
            do {
               try value.write(to: fileUrl, atomically: true, encoding: String.Encoding.utf8)
            } catch let error as NSError {
               print (error)
            }
            
            do {
               readFile = try String(contentsOf: fileUrl)
            } catch let error as NSError {
               print(error)
            }
            
            activityPrediction()
            
            if readFile.isEmpty == false {
            print("Hello bye bye")
            self.classlabel.text = activityPrediction2() ?? "N/A"
            appDelegate.shots.append(self.classlabel.text ?? "N/A"
            )
           
            updateChartData()
            self.count = count + 1

            
    
            line_entries.removeAll()
            
            for x in 0...shotlength {
                line_entries.append(BarChartDataEntry(x: Double(x)/sensorfreq, y: appDelegate.rotX_edit[x]))
            }
            updateLineChart(line_entries: line_entries, name: "X Rotation")
            }
            
            print(appDelegate.shots)
            print(appDelegate.stats)

            
        
          }
    }
  }
    
}



//MARK: Other Extensions


extension Collection where Iterator.Element == String {
    var doubleArray: [Double] {
        return compactMap{ Double($0) }
    }
    var floatArray: [Float] {
        return compactMap{ Float($0) }
    }
}


extension UILabel {
    @IBInspectable
    var rotation: Int {
        get {
            return 0
        } set {
            let radians = CGFloat(CGFloat(Double.pi) * CGFloat(newValue) / CGFloat(180.0))
            self.transform = CGAffineTransform(rotationAngle: radians)
        }
    }
}


extension Date {
    var millisecondsSince1970:Int64 {
        return Int64((self.timeIntervalSince1970 * 1000.0).rounded())
    }
}


extension UIImage {
    func toPngString() -> String? {
        let data = self.pngData()
        return data?.base64EncodedString(options: .endLineWithLineFeed)
    }
}


