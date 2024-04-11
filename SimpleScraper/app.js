const { handleClubv1 } = require("./clubv1");

exports.handler = async (event, context) => {
  try {
    let body = event.body;
    if (event.isBase64Encoded) {
      const decodedBody = Buffer.from(body, "base64").toString("utf-8");
      body = JSON.parse(decodedBody);
    } else {
      body = JSON.parse(body);
    }
    console.log(body);
    const platform = body.platform;
    if (platform === "clubv1") {
      console.log("Handling clubv1 platform");
      return await handleClubv1(body);
    } else {
      console.log("Unsupported platform");
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Unsupported platform" }),
      };
    }
  } catch (error) {
    const errorMessage = "An error occurred while processing the request.";
    console.log(errorMessage);
    console.log(error.stack);
    return { statusCode: 500, body: JSON.stringify({ message: errorMessage }) };
  }
}