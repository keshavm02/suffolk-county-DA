//  ViewController.swift
//  test
//  Created by Masayoshi Iwasa on 11/9/19.
//  Copyright © 2019 Masayoshi Iwasa. All rights reserved.
//
import UIKit
import SafariServices

class ViewController: UIViewController, UIImagePickerControllerDelegate,
UINavigationControllerDelegate,UIPickerViewDelegate, UIPickerViewDataSource,
    SFSafariViewControllerDelegate,UITextFieldDelegate
{
    
    
    @IBOutlet var cameraView : UIImageView!
    
    @IBOutlet weak var resultLabel: UILabel!
    
    @IBOutlet weak var mylabel: UILabel?
    //    Dropdown menu for document types
    @IBOutlet weak var documentType: UIPickerView?
    
    
//    @IBOutlet weak var textView: UITextView?
    
    var pickerData: [String] = [String]()
    var respondJSON : String = "";
    var pickedDocument : String = "";
    var fixedJSON : String = "";
    
    
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // overrideUserInterfaceStyle is available with iOS 13
        if #available(iOS 13.0, *) {
               // Always adopt a light interface style.
               overrideUserInterfaceStyle = .light
        }
        
        mylabel?.numberOfLines = 2
        mylabel?.lineBreakMode = NSLineBreakMode.byWordWrapping

        mylabel?.text = "Tap Capture Image or Access Library first, then choose type of document, and Scan Document"
        // Connect data:
        documentType?.delegate = self
        documentType?.dataSource = self
        
//        textView?.isSelectable = true
//        textView?.isEditable = false
        
        
//        listenforchange()
//        if respondJSON != "" {
//            textView?.text = respondJSON
//        }
//        else{
//            textView?.text = "Loading..."
//        }
        
        resultLabel?.text = "Completed!"
        
        // Input the data into the array
        pickerData = ["-","Application for Criminal Complaint (Court)", "Application for Criminal Complaint (Justice Department)", "Police Department Arrest Booking Form", "Arrest Report", "Offense/Incident Report", "Supplemental Report", "Criminal Complaint", "Incident Report", "Court Activity Record Information"]
        
        
        
    }
    
    func numberOfComponents(in pickerView: UIPickerView) -> Int {
        return 1
    }
    
    func pickerView(_ pickerView: UIPickerView, numberOfRowsInComponent component: Int) -> Int {
        return pickerData.count
    }
    
    func pickerView(_ pickerView: UIPickerView, attributedTitleForRow row: Int, forComponent component: Int) -> NSAttributedString? {
        
        return NSAttributedString(string: pickerData[row], attributes: [NSAttributedString.Key.font:UIFont(name: "Georgia", size: 30.0)!,NSAttributedString.Key.foregroundColor:UIColor.white])
    }
    
    func pickerView(_ pickerView: UIPickerView, didSelectRow row: Int, inComponent component: Int) {
        self.pickedDocument = pickerData[row]
        print(self.pickedDocument)
    }
    
    @IBAction func openURL(_ sender: Any) {
        // check if website exists

        guard let url = URL(string: "http://localhost:5000/all_cases") else {
            return
            
        }

        let safariVC = SFSafariViewController(url: url)
        present(safariVC, animated: true, completion: nil)
        
        safariVC.delegate = self
    }
    
    func safariViewControllerDidFinish(_ controller: SFSafariViewController) {
        controller.dismiss(animated: true, completion: nil)
    }
    
    // Open camera
    @IBAction func startCamera(_ sender : AnyObject) {
        
        let sourceType:UIImagePickerController.SourceType =
            UIImagePickerController.SourceType.camera
        // check if camera is available
        if UIImagePickerController.isSourceTypeAvailable(
            UIImagePickerController.SourceType.camera){
            // initiate camera picker
            let cameraPicker = UIImagePickerController()
            cameraPicker.sourceType = sourceType
            cameraPicker.delegate = self
            self.present(cameraPicker, animated: true, completion: nil)
            
        }
        else{
            mylabel?.text = "error"
            
        }
    }
    
    //　call this after taking a photo
    func imagePickerController(_ imagePicker: UIImagePickerController,
            didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]){
        
        if let pickedImage = info[.originalImage]
            as? UIImage {
            
            
            // get screen Size


            let screenWidth = self.view.bounds.width
            let screenHeight = self.view.bounds.height
            
            
            
            // image width and height
            let width = cameraView.bounds.size.width
            let height = cameraView.bounds.size.height
            
            
            // adjust image size to the screen size
            let scale = screenWidth / width
            
            let rect:CGRect = CGRect(x:0, y:0, width:width*scale, height:height*scale)
            
            // fit cameraView frame to CGRect
            cameraView.frame = rect;
            
            // centering the image
            cameraView.center = CGPoint(x:screenWidth/2, y:screenHeight/3)
            

            cameraView.image = pickedImage
        }

        //closing
        imagePicker.dismiss(animated: true, completion: nil)
        mylabel?.text = "Tap Scan Image once the image is ready!"
        
    }
    
    
    // Call this when cancelled
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        picker.dismiss(animated: true, completion: nil)
        mylabel?.text = "Canceled"
    }
    
    
    // Save images
    @IBAction func savePicture(_ sender : AnyObject) {
        let image:UIImage! = cameraView.image
        
        if image != nil {
            UIImageWriteToSavedPhotosAlbum(
                image,
                self,
                #selector(ViewController.image(_:didFinishSavingWithError:contextInfo:)),
                nil)
        }
        else{
            mylabel?.text = "image Failed !"
        }
    }
    
    
    
    // result of writting image
    @objc func image(_ image: UIImage,
                     didFinishSavingWithError error: NSError!,
                     contextInfo: UnsafeMutableRawPointer) {
        
        if error != nil {
            print(error.code)
            mylabel?.text = "Scan Failed !"
        }
        else{
            mylabel?.text = "Scan Sent"
        }
    }
    
    
    // show album
    @IBAction func showAlbum(_ sender : AnyObject) {
        let sourceType:UIImagePickerController.SourceType =
            UIImagePickerController.SourceType.photoLibrary
        
        if UIImagePickerController.isSourceTypeAvailable(
            UIImagePickerController.SourceType.photoLibrary){
            // initiate camera picker
            let cameraPicker = UIImagePickerController()
            cameraPicker.sourceType = sourceType
            cameraPicker.delegate = self
            self.present(cameraPicker, animated: true, completion: nil)
            
            mylabel?.text = "Tap the [Start] to save a document"
        }
        else{
            mylabel?.text = "error"
            
        }
        
    }
    
    func routing() -> String{
        let picked = self.pickedDocument
        let iproute = "http://localhost:5000:5000"
        if picked == "Criminal Complaint" {
            return "\(iproute)/CC"
        } else if picked == "Police Department Arrest Booking Form"{
            return "\(iproute)/ABF"
        } else {
            return "\(iproute)"

        }
    }
    
    func convertToDictionary(text: String) -> [String: Any]? {
        if let data = text.data(using: .utf8) {
            do {
                return try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
            } catch {
                print(error.localizedDescription)
            }
        }
        return nil
    }
    
    func convertToJson(from object:Any) -> String? {
        guard let data = try? JSONSerialization.data(withJSONObject: object, options: []) else {
            return nil
        }
        return String(data: data, encoding: String.Encoding.utf8)
    }
    @IBAction func uploadFixed(sender: AnyObject){
        guard let image = cameraView.image?.jpegData(compressionQuality: 0.8) else { return  }
        let filename = "file.jpeg"
        let boundary = UUID().uuidString


        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)

        // Set the URLRequest to POST and to the specified URL

        var urlRequest = URLRequest(url: URL(string: "http://localhost:5000/confirm_CC")!)

        urlRequest.httpMethod = "POST"

        // Set Content-Type Header to multipart/form-data, this is equivalent to submitting form data with file upload in a web browser
        // And the boundary is also set here
        urlRequest.setValue("multipart/form-data;boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var data = Data()
        
        let json = convertToJson(from: self.fixedJSON)
        data.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
        data.append("Content-Disposition: form-data; name=\"data\"\r\n\r\n".data(using: .utf8)!)
        data.append("\(String(describing: json))\r\n".data(using: .utf8)!)
        

        // Add the image data to the raw http request data
        data.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
        data.append("Content-Disposition: form-data;name=\"file\";filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        data.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        data.append(image)

        data.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        print("")
        // Send a POST request to the URL, with the data we created earlier
        session.uploadTask(with: urlRequest, from: data, completionHandler: { responseData, response, error in
            
            if(error != nil){
                print("\(error!.localizedDescription)")
            }
            
            guard let responseData = responseData else {
                print("no response data")
                return
            }
            
            if let responseString = String(data: responseData, encoding: .utf8) {
                
                self.respondJSON = responseString;
                print("uploaded to: \(responseString)")
            }
        }).resume()
        
        
    }
    
    
    
    @IBAction func upload(sender: AnyObject) {
        
        // the image in UIImage type
        guard let image = cameraView.image?.jpegData(compressionQuality: 1.0) else { return  }
        let filename = "file.jpeg"

        // generate boundary string using a unique per-app string
        let boundary = UUID().uuidString


        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)

        // Set the URLRequest to POST and to the specified URL
        let routeUrl = routing()
        var urlRequest = URLRequest(url: URL(string: routeUrl)!)
        urlRequest.httpMethod = "POST"

        // Set Content-Type Header to multipart/form-data, this is equivalent to submitting form data with file upload in a web browser
        // And the boundary is also set here
        urlRequest.setValue("multipart/form-data;boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var data = Data()


        // Add the image data to the raw http request data
        data.append("\r\n--\(boundary)\r\n".data(using: .utf8)!)
        data.append("Content-Disposition: form-data;name=\"file\";filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        data.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        data.append(image)

        data.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)
        print(routeUrl)
        // Send a POST request to the URL, with the data we created earlier
        mylabel?.text = "Uploading..."
        session.uploadTask(with: urlRequest, from: data, completionHandler: { responseData, response, error in
            
            if(error != nil){
                print("\(error!.localizedDescription)")
            }
            
            guard let responseData = responseData else {
                print("no response data")
                return
            }
            
            if let responseString = String(data: responseData, encoding: .utf8) {
                
                self.respondJSON = responseString;
                print("uploaded to: \(responseString)")
//                self.textView?.text = responseString
//                self.textView?.insertText(self.respondJSON)
                
            }
        }).resume()
        
        
    }
    
    
//    func listenforchange() {
//        print("listening...")
//        DispatchQueue.main.async {
//            if self.respondJSON != "" {
//                self.textView?.text = self.respondJSON
//            }
//        }
        
        
//    }
    
}
